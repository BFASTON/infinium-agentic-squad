#!/usr/bin/env python3
"""Validate the marketplace, plugin manifest, agents and commands.

Run from the repo root: python3 scripts/validate.py
Exits non-zero on any problem. Uses only the standard library.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "infinium-squad"
VALID_MODELS = {"inherit", "sonnet", "opus", "haiku"}
COMMUNITY_REGISTER = PLUGIN / "skills" / "infinium-standards" / "standards" / "community-tools.md"
# Agent Skills specification (https://agentskills.io/specification)
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SKILL_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
errors: list[str] = []


def frontmatter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}
    data = {}
    key = None
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            key, data[k.strip()] = k.strip(), v.strip()
        elif key and line.startswith(" ") and data[key] in ("|", ">", "|-", ">-", ""):
            # Block scalar (description: |) or nested map (metadata:); keep the text.
            data[key + "\0"] = (data.get(key + "\0", "") + " " + line.strip()).strip()
    for k in [k for k in data if k.endswith("\0")]:
        base = k[:-1]
        if data[base] in ("|", ">", "|-", ">-"):
            data[base] = data[k]
        del data[k]
    if not text[m.end():].strip():
        errors.append(f"{path.relative_to(ROOT)}: empty body")
    return data


def load_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        errors.append(f"{path.relative_to(ROOT)}: {e}")
        return {}


market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
load_json(PLUGIN / "hooks" / "hooks.json")

# Every marketplace entry: local plugins must exist with matching name and
# version; external plugins must be pinned to a full commit SHA (supply chain).
local_plugin_dirs = []
for entry in market.get("plugins", []):
    src = entry.get("source")
    name = entry.get("name")
    if isinstance(src, str):
        pdir = (ROOT / src).resolve()
        manifest = load_json(pdir / ".claude-plugin" / "plugin.json") if pdir.is_dir() else {}
        if not manifest:
            errors.append(f"marketplace.json: plugin '{name}' source {src} has no plugin.json")
            continue
        local_plugin_dirs.append(pdir)
        if manifest.get("name") != name:
            errors.append(f"marketplace.json: entry '{name}' does not match plugin.json name '{manifest.get('name')}'")
        if entry.get("version") != manifest.get("version"):
            errors.append(f"version mismatch for {name}: marketplace {entry.get('version')} vs plugin {manifest.get('version')}")
    elif isinstance(src, dict):
        if not re.fullmatch(r"[0-9a-f]{40}", str(src.get("sha", ""))):
            errors.append(f"marketplace.json: external plugin '{name}' must be pinned with a 40-character commit 'sha'")
        if name not in COMMUNITY_REGISTER.read_text(encoding="utf-8"):
            errors.append(f"marketplace.json: external plugin '{name}' is not listed in the Community Tools Register")
    else:
        errors.append(f"marketplace.json: plugin '{name}' has no valid source")
if PLUGIN.resolve() not in local_plugin_dirs:
    errors.append("marketplace.json: no entry for plugin infinium-squad")

agents = sorted((PLUGIN / "agents").glob("*.md"))
names = set()
for a in agents:
    fm = frontmatter(a)
    rel = a.relative_to(ROOT)
    if fm.get("name") != a.stem:
        errors.append(f"{rel}: name '{fm.get('name')}' must match file name '{a.stem}'")
    if len(fm.get("description", "")) < 40:
        errors.append(f"{rel}: description missing or too short to route on")
    if fm.get("model", "inherit") not in VALID_MODELS:
        errors.append(f"{rel}: invalid model '{fm.get('model')}'")
    names.add(fm.get("name"))

for c in sorted((PLUGIN / "commands").glob("*.md")):
    if not frontmatter(c).get("description"):
        errors.append(f"{c.relative_to(ROOT)}: missing description")
    for ref in re.findall(r"`([a-z]+(?:-[a-z]+)+)` agent", c.read_text(encoding="utf-8")):
        if ref not in names:
            errors.append(f"{c.relative_to(ROOT)}: references unknown agent '{ref}'")

skills = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
all_skills = sorted(s for d in local_plugin_dirs for s in (d / "skills").glob("*/SKILL.md"))
for s in all_skills:
    rel = s.relative_to(ROOT)
    fm = frontmatter(s)
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != s.parent.name:
        errors.append(f"{rel}: name '{name}' must match folder name '{s.parent.name}'")
    if not (SKILL_NAME.fullmatch(name) and len(name) <= 64):
        errors.append(f"{rel}: name must be 1-64 lowercase letters, digits and single hyphens (Agent Skills spec)")
    if len(desc) < 40:
        errors.append(f"{rel}: description missing or too short to route on")
    if len(desc) > 1024:
        errors.append(f"{rel}: description over 1024 characters (Agent Skills spec)")
    for field in set(fm) - SKILL_FIELDS:
        errors.append(f"{rel}: frontmatter field '{field}' is not in the Agent Skills spec; put it under metadata")
for s in skills:
    rel = s.relative_to(ROOT)
    text = s.read_text(encoding="utf-8")
    for link in re.findall(r"\]\((standards/[^)]+)\)", text):
        if not (s.parent / link).exists():
            errors.append(f"{rel} links to missing file {link}")

# Relative links between standards documents must resolve.
for doc in sorted((PLUGIN / "skills" / "infinium-standards" / "standards").glob("*.md")):
    for link in re.findall(r"\]\(([^)#:]+\.md)(?:#[^)]*)?\)", doc.read_text(encoding="utf-8")):
        if not (doc.parent / link).exists():
            errors.append(f"{doc.relative_to(ROOT)} links to missing file {link}")

# Agent names written in backticks in agent, command and skill bodies must exist.
skill_names = {s.parent.name for s in skills}
for f in [*agents, *sorted((PLUGIN / "commands").glob("*.md")), *skills]:
    for ref in set(re.findall(r"`([a-z]+(?:-[a-z]+)+)`", f.read_text(encoding="utf-8"))):
        looks_like_agent = ref.endswith(("-engineer", "-reviewer", "-specialist", "-lead", "-writer", "-validator", "-critic", "-judge"))
        if looks_like_agent and ref not in names:
            errors.append(f"{f.relative_to(ROOT)}: references unknown agent '{ref}'")
        if ref.endswith(("-protocol", "-standards")) and ref not in skill_names:
            errors.append(f"{f.relative_to(ROOT)}: references unknown skill '{ref}'")

if errors:
    print("Validation failed:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"OK: {len(agents)} agents, {len(list((PLUGIN / 'commands').glob('*.md')))} commands, {len(all_skills)} skills across {len(local_plugin_dirs)} local plugins, {len(market.get('plugins', [])) - len(local_plugin_dirs)} pinned external plugin(s), manifests valid.")
