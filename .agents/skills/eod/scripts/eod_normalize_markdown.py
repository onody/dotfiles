#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re


ROOT = Path("/Users/onod/src/memo")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+$", "", line) for line in text.split("\n")]

    normalized: list[str] = []
    blank_run = 0
    for line in lines:
        if line == "":
            blank_run += 1
            if blank_run <= 1:
                normalized.append("")
            continue
        blank_run = 0
        normalized.append(line)

    return "\n".join(normalized).strip("\n") + "\n"


def process_file(path: Path) -> bool:
    original = path.read_text()
    updated = normalize_text(original)
    if updated == original:
        return False
    path.write_text(updated)
    return True


def main() -> None:
    import sys

    changed: list[Path] = []
    targets = [Path(arg) for arg in sys.argv[1:]]
    if not targets:
        print("No target files.")
        return

    for path in targets:
        full_path = path if path.is_absolute() else ROOT / path
        if not full_path.exists() or full_path.suffix != ".md":
            continue
        if process_file(full_path):
            changed.append(full_path)

    if not changed:
        print("No markdown normalization changes.")
        return

    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
