#!/usr/bin/env python3
"""Claude Code Notification hook: push a phone alert when the squad needs a human.

Claude Code raises a Notification when it needs permission for a tool or has
been waiting for your input. This hook forwards that to ntfy or Pushover so
you can step away from the terminal (Escalation Policy section 5).

Configured per user through environment variables. Nothing is sent unless
INFINIUM_NOTIFY is set. No secrets live in this repository.

  INFINIUM_NOTIFY            "ntfy" or "pushover" (unset or "off": do nothing)
  INFINIUM_NOTIFY_DETAIL     "1" to include the project folder name (default: off)

  ntfy:
  NTFY_TOPIC                 required; use a long random topic name
  NTFY_SERVER                default https://ntfy.sh (use your own server if you have one)
  NTFY_TOKEN                 optional access token for a protected topic

  Pushover:
  PUSHOVER_APP_TOKEN         required
  PUSHOVER_USER_KEY          required

The push never contains code, prompts, tool input or Claude's message text:
only a generic line about why Claude is waiting. Failures are ignored so the
hook can never block a session. Standard library only.
"""
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

TIMEOUT_SECONDS = 5
TITLE = "Claude needs you"
REASONS = {
    "permission_prompt": "Claude is waiting for your approval.",
    "idle_prompt": "Claude has a question or is waiting for your input.",
    "elicitation_dialog": "Claude is asking you for input.",
}
SKIP = {"auth_success"}


def build_message(event: dict) -> str | None:
    kind = event.get("notification_type") or ""
    if kind in SKIP:
        return None
    text = REASONS.get(kind, "Claude is waiting for you.")
    if os.environ.get("INFINIUM_NOTIFY_DETAIL") == "1" and event.get("cwd"):
        text += f" Project: {pathlib.Path(event['cwd']).name}"
    return text


def send_ntfy(text: str) -> None:
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if not topic:
        raise ValueError("NTFY_TOPIC is not set")
    server = os.environ.get("NTFY_SERVER", "https://ntfy.sh").rstrip("/")
    if not server.startswith("https://"):
        raise ValueError("NTFY_SERVER must use https")
    req = urllib.request.Request(
        f"{server}/{urllib.parse.quote(topic, safe='')}",
        data=text.encode("utf-8"),
        headers={"Title": TITLE, "Priority": "high", "Tags": "robot"},
        method="POST",
    )
    token = os.environ.get("NTFY_TOKEN", "").strip()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS).close()


def send_pushover(text: str) -> None:
    app = os.environ.get("PUSHOVER_APP_TOKEN", "").strip()
    user = os.environ.get("PUSHOVER_USER_KEY", "").strip()
    if not (app and user):
        raise ValueError("PUSHOVER_APP_TOKEN and PUSHOVER_USER_KEY must be set")
    body = urllib.parse.urlencode(
        {"token": app, "user": user, "title": TITLE, "message": text}
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://api.pushover.net/1/messages.json", data=body, method="POST"
    )
    urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS).close()


SENDERS = {"ntfy": send_ntfy, "pushover": send_pushover}


def main() -> int:
    service = os.environ.get("INFINIUM_NOTIFY", "").strip().lower()
    if service in ("", "off", "none", "0"):
        return 0
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        event = {}
    text = build_message(event if isinstance(event, dict) else {})
    if text is None:
        return 0
    sender = SENDERS.get(service)
    if sender is None:
        print(f"notify_human: unknown INFINIUM_NOTIFY '{service}'", file=sys.stderr)
        return 0
    try:
        sender(text)
    except Exception as e:  # never block the session on a notification failure
        print(f"notify_human: push not sent ({type(e).__name__}: {e})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
