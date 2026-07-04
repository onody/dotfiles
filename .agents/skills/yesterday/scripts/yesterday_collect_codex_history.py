#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import sqlite3
from pathlib import Path


REPO_ROOT = "/Users/onod/src/memo"
CODEX_DIR = Path("/Users/onod/.dotfiles/.codex")
HISTORY_PATH = CODEX_DIR / "history.jsonl"
STATE_DB_PATH = CODEX_DIR / "state_5.sqlite"
TZ = dt.timezone(dt.timedelta(hours=9))


def target_day_range_epoch(target_date: str | None = None) -> tuple[int, int, str]:
    if target_date:
        start = dt.datetime.combine(dt.date.fromisoformat(target_date), dt.time.min, tzinfo=TZ)
    else:
        today = dt.datetime.now(TZ).replace(hour=0, minute=0, second=0, microsecond=0)
        start = today - dt.timedelta(days=1)
    end = start + dt.timedelta(days=1)
    return int(start.timestamp()), int(end.timestamp()), start.date().isoformat()


def load_repo_threads(start_ts: int, end_ts: int) -> list[tuple[str, str, str]]:
    conn = sqlite3.connect(str(STATE_DB_PATH))
    try:
        cur = conn.execute(
            """
            select id, title, preview
            from threads
            where cwd = ?
              and updated_at >= ?
              and updated_at < ?
            """,
            (REPO_ROOT, start_ts, end_ts),
        )
        return [(row[0], row[1] or "", row[2] or "") for row in cur.fetchall()]
    finally:
        conn.close()


def load_history(thread_ids: set[str], start_ts: int, end_ts: int) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    if not HISTORY_PATH.exists():
        return results

    with HISTORY_PATH.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            session_id = row.get("session_id")
            ts = row.get("ts")
            text = (row.get("text") or "").strip()
            if session_id not in thread_ids:
                continue
            if not isinstance(ts, int) or ts < start_ts or ts >= end_ts:
                continue
            if not text or text.lower() == "exit":
                continue
            key = (session_id, text)
            if key in seen:
                continue
            seen.add(key)
            results.append((session_id, text))
    return results


def main() -> None:
    import sys

    target_date = sys.argv[1] if len(sys.argv) > 1 else None
    start_ts, end_ts, iso_date = target_day_range_epoch(target_date)
    threads = load_repo_threads(start_ts, end_ts)
    thread_ids = {thread_id for thread_id, _, _ in threads}
    items = load_history(thread_ids, start_ts, end_ts)
    if not items and not threads:
        print("NO_TARGET_DAY_CODEX_MESSAGES")
        return

    print(f"# codex-session {iso_date}")
    for session_id, text in items:
        print(f"[user][{session_id}] {text}")
        print()

    seen_item_threads = {session_id for session_id, _ in items}
    for thread_id, title, preview in threads:
        if thread_id in seen_item_threads:
            continue
        fallback = preview.strip() or title.strip()
        if not fallback:
            continue
        print(f"[thread-preview][{thread_id}] {fallback}")
        print()


if __name__ == "__main__":
    main()
