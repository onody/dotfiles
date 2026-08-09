#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import glob
import json
import os
import sys

TZ = dt.timezone(dt.timedelta(hours=9))
PROJECTS_ROOT = os.path.expanduser("~/.claude/projects/")
AUTO_TRIGGER_PREFIX = "summarizeが完了しました"


def target_day(target_date: str | None = None) -> str:
    if target_date:
        return target_date
    return (dt.datetime.now(TZ) - dt.timedelta(days=1)).date().isoformat()


def extract_text(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return " ".join(
            part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") == "text"
        ).strip()
    return ""


def is_auto_triggered_session(lines: list[dict]) -> bool:
    """True if this session was kicked off by auto-diary's headless `claude -p` call.

    Those sessions are the yesterday routine running on itself: their transcript is
    the skill's own instructions and tool chatter, not organic conversation, so they
    must never be presented as ingest material.
    """
    for entry in lines:
        if entry.get("type") != "user":
            continue
        text = extract_text(entry.get("message", {}).get("content", ""))
        if text:
            return text.startswith(AUTO_TRIGGER_PREFIX)
    return False


def main() -> None:
    target_date = sys.argv[1] if len(sys.argv) > 1 else None
    iso_date = target_day(target_date)

    found = False
    for project_dir in sorted(glob.glob(PROJECTS_ROOT + "*/")):
        project_name = os.path.basename(os.path.normpath(project_dir))
        if not project_name.startswith("-Users-onod-"):
            # Excludes e.g. the bare "-" project (cwd "/"), which is thousands of
            # one-shot screenshot-captioning sessions from auto-diary automation,
            # not organic conversation.
            continue
        for path in sorted(glob.glob(project_dir + "*.jsonl")):
            try:
                lines = [json.loads(line) for line in open(path) if line.strip()]
            except (OSError, json.JSONDecodeError):
                continue

            if is_auto_triggered_session(lines):
                continue

            messages: list[tuple[str, str]] = []
            for entry in lines:
                if not entry.get("timestamp", "").startswith(iso_date):
                    continue
                if entry.get("type") not in ("user", "assistant"):
                    continue
                text = extract_text(entry.get("message", {}).get("content", ""))
                if text:
                    messages.append((entry["type"], text[:800]))

            if messages:
                found = True
                print(f"# claude-session {iso_date} ({project_name})")
                for role, text in messages:
                    print(f"[{role}] {text}")
                    print()
                print("===")

    if not found:
        print("NO_TARGET_DAY_CLAUDE_MESSAGES")


if __name__ == "__main__":
    main()
