#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import glob
import json
import os
import sys

TZ = dt.timezone(dt.timedelta(hours=9))
PROJECT_DIR = os.path.expanduser("~/.claude/projects/-Users-onod-src-memo/")


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


def main() -> None:
    target_date = sys.argv[1] if len(sys.argv) > 1 else None
    iso_date = target_day(target_date)

    found = False
    for path in sorted(glob.glob(PROJECT_DIR + "*.jsonl")):
        messages: list[tuple[str, str]] = []
        try:
            lines = [json.loads(line) for line in open(path) if line.strip()]
        except (OSError, json.JSONDecodeError):
            continue

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
            print(f"# claude-session {iso_date}")
            for role, text in messages:
                print(f"[{role}] {text}")
                print()
            print("===")

    if not found:
        print("NO_TARGET_DAY_CLAUDE_MESSAGES")


if __name__ == "__main__":
    main()
