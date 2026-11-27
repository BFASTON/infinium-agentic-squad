#!/usr/bin/env python3
"""PreToolUse guardrail: stop agents reading or writing files that usually hold secrets.

Exit code 2 blocks the tool call and shows the message to Claude.
Template files such as `.env.example` are allowed.
"""
import json
import os
import re
import sys

BLOCKED = [
    r"(^|/)\.env(\.[^/]*)?$",
    r"\.pem$",
    r"\.key$",
    r"\.p12$",
    r"\.pfx$",
    r"(^|/)id_(rsa|ed25519|ecdsa)$",
    r"(^|/)\.aws/credentials$",
    r"(^|/)\.npmrc$",
    r"(^|/)\.pypirc$",
    r"(^|/)secrets?\.(json|ya?ml|toml)$",
    r"\.tfstate(\.backup)?$",
]
ALLOWED = [r"\.example$", r"\.sample$", r"\.template$", r"(^|/)\.env\.dist$"]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    path = (data.get("tool_input") or {}).get("file_path", "")
    if not path:
        return 0
    norm = path.replace(os.sep, "/")
    if any(re.search(p, norm) for p in ALLOWED):
        return 0
    if any(re.search(p, norm, re.IGNORECASE) for p in BLOCKED):
        print(
            f"Blocked by Infinium security policy: '{path}' looks like a secrets file. "
            "Agents must not read or write credentials. Use the approved secrets manager "
            "and reference secrets by name (see the Infinium Security Guide, section 3).",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
