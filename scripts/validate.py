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
errors: list[str] = []


def frontmatter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}
    data = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
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
plugin = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
load_json(PLUGIN / "hooks" / "hooks.json")

entry = next((p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")), None)
if not entry:
    errors.append("marketplace.json: no entry for plugin " + str(plugin.get("name")))
elif entry.get("version") != plugin.get("version"):
    errors.append(f"version mismatch: marketplace {entry.get('version')} vs plugin {plugin.get('version')}")

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
for s in skills:
    rel = s.relative_to(ROOT)
    fm = frontmatter(s)
    if fm.get("name") != s.parent.name:
        errors.append(f"{rel}: name '{fm.get('name')}' must match folder name '{s.parent.name}'")
    if len(fm.get("description", "")) < 40:
        errors.append(f"{rel}: description missing or too short to route on")
    text = s.read_text(encoding="utf-8")
    for link in re.findall(r"\]\((standards/[^)]+)\)", text):
        if not (s.parent / link).exists():
            errors.append(f"{rel} links to missing file {link}")

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
print(f"OK: {len(agents)} agents, {len(list((PLUGIN / 'commands').glob('*.md')))} commands, {len(skills)} skills, manifests valid.")
