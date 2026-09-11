#!/usr/bin/env python3
"""yesterday skill の Step1(ファイル名整理) + Step2(リンク検証) をまとめて実行する。

機械的に安全な操作(raw/直下の日付ファイル移動、training移動、clippingの
kebab-case化とそれに伴うリンク参照の書き換え)のみ自動実行する。
判断が必要なもの(kebab-case化できない名前、壊れたリンク)は一切書き換えず、
レポートのみ出力する。

--dry-run を付けると実際のファイル操作を行わず、何が起きるかだけ表示する。
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path("/Users/onod/src/memo")
RAW_DIR = REPO_ROOT / "raw"
DIARY_DIR = RAW_DIR / "diary"
CLIPPING_DIR = RAW_DIR / "clipping"
TRAINING_DIR = RAW_DIR / "training"
WIKI_DIR = REPO_ROOT / "wiki"

DIARY_NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
TRAINING_NAME_RE = re.compile(r"^training-(\d{4}-\d{2})\.md$")
KEBAB_RE = re.compile(r"^[a-z0-9-]+\.md$")
LINK_RE = re.compile(r"\[\[([^\]|]+)(\|[^\]]*)?\]\]")

DRY_RUN = False


def is_tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "--error-unmatch", str(path.relative_to(REPO_ROOT))],
        capture_output=True,
    )
    return result.returncode == 0


def move(src: Path, dst: Path) -> None:
    if DRY_RUN:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if is_tracked(src):
        subprocess.run(
            ["git", "-C", str(REPO_ROOT), "mv", str(src.relative_to(REPO_ROOT)), str(dst.relative_to(REPO_ROOT))],
            check=True,
        )
    else:
        src.rename(dst)


def normalize_clipping_name(name: str) -> str:
    stem = name[:-3] if name.endswith(".md") else name
    stem = stem.lower()
    stem = re.sub(r"\s+", "-", stem)
    stem = re.sub(r"[^a-z0-9\-]", "", stem)
    stem = re.sub(r"-+", "-", stem).strip("-")
    return f"{stem}.md"


def update_diary_links(old_stem: str, new_stem: str) -> list[str]:
    updated = []
    pattern = re.compile(r"\[\[" + re.escape(old_stem) + r"(\|[^\]]*)?\]\]")
    if not DIARY_DIR.exists():
        return updated
    for diary_path in sorted(DIARY_DIR.glob("*.md")):
        text = diary_path.read_text()
        new_text, n = pattern.subn(lambda m: f"[[{new_stem}{m.group(1) or ''}]]", text)
        if n:
            if not DRY_RUN:
                diary_path.write_text(new_text)
            updated.append(f"{diary_path.name}({n}箇所)")
    return updated


def step1() -> tuple[list[str], list[str]]:
    auto_fixed: list[str] = []
    needs_review: list[str] = []

    if not RAW_DIR.exists():
        return auto_fixed, needs_review

    for f in sorted(RAW_DIR.glob("*.md")):
        if DIARY_NAME_RE.match(f.name):
            dst = DIARY_DIR / f.name
            move(f, dst)
            auto_fixed.append(f"raw/{f.name} → raw/diary/{f.name}")
        elif (m := TRAINING_NAME_RE.match(f.name)):
            dst = TRAINING_DIR / f"{m.group(1)}.md"
            move(f, dst)
            auto_fixed.append(f"raw/{f.name} → raw/training/{m.group(1)}.md")

    if CLIPPING_DIR.exists():
        for f in sorted(CLIPPING_DIR.glob("*.md")):
            if KEBAB_RE.match(f.name):
                continue
            new_name = normalize_clipping_name(f.name)
            if new_name == f.name or not KEBAB_RE.match(new_name):
                needs_review.append(
                    f"raw/clipping/{f.name} — kebab-case化不能(非ASCII文字などが残る)。"
                    f"内容から英語kebab-case名へ翻訳してrenameし、参照リンクは新ファイル名を指しつつ"
                    f"表示名は元の名前を保持する([[新名|{f.stem}]])こと"
                )
                continue
            old_stem, new_stem = f.stem, new_name[:-3]
            move(f, CLIPPING_DIR / new_name)
            auto_fixed.append(f"raw/clipping/{f.name} → raw/clipping/{new_name}")
            link_updates = update_diary_links(old_stem, new_stem)
            if link_updates:
                auto_fixed.append(f"  リンク参照更新: {', '.join(link_updates)}")

    # raw/直下のその他ファイルは自動修正しない。違反のみ報告する。
    for f in sorted(RAW_DIR.glob("*.md")):
        if not KEBAB_RE.match(f.name):
            if not f.name.isascii():
                needs_review.append(
                    f"raw/{f.name} — マルチバイトファイル名。内容から英語kebab-case名へ翻訳してrenameし、"
                    f"参照リンクは新ファイル名を指しつつ表示名は元の名前を保持する([[新名|{f.stem}]])こと"
                )
            else:
                needs_review.append(f"raw/{f.name} — english-lowercase-kebab-case形式ではない(自動修正なし)")

    return auto_fixed, needs_review


def existing_stems() -> set[str]:
    stems: set[str] = set()
    if RAW_DIR.exists():
        stems |= {p.stem for p in RAW_DIR.rglob("*.md")}
    if WIKI_DIR.exists():
        stems |= {p.stem for p in WIKI_DIR.glob("*.md")}
    return stems


def step2() -> list[str]:
    broken: list[str] = []
    valid_stems = existing_stems()
    targets = []
    if WIKI_DIR.exists():
        targets += sorted(WIKI_DIR.glob("*.md"))
    if DIARY_DIR.exists():
        targets += sorted(DIARY_DIR.glob("*.md"))
    for path in targets:
        text = path.read_text()
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip()
            if target not in valid_stems:
                broken.append(f"{path.relative_to(REPO_ROOT)}: [[{target}]] — リンク先が見つからない")
    return broken


def main() -> None:
    global DRY_RUN
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="ファイル操作を行わず表示のみ")
    args = parser.parse_args()
    DRY_RUN = args.dry_run

    auto_fixed, needs_review = step1()
    broken_links = step2()

    prefix = "[dry-run] " if DRY_RUN else ""

    print(f"{prefix}## Step1: 自動修正済み")
    for line in auto_fixed or ["(なし)"]:
        print(f"- {line}")

    print(f"\n{prefix}## Step1: 要判断(自動修正なし)")
    for line in needs_review or ["(なし)"]:
        print(f"- {line}")

    print(f"\n{prefix}## Step2: 壊れたリンク")
    for line in broken_links or ["(なし)"]:
        print(f"- {line}")


if __name__ == "__main__":
    main()
