#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path("/Users/onod/src/memo")
PLACES_PATH = REPO_ROOT / "wiki/places.md"
DIARY_DIR = REPO_ROOT / "raw/diary"
USER_AGENT = "Mozilla/5.0 (compatible; Yesterday Places Sync)"

KEYWORDS = ("行きたい", "行ってみたい", "食べたい", "泊まりたい", "絶対次食べる")
FOOD_DOMAINS = ("tabelog.com", "s.tabelog.com", "ramendb.supleks.jp")
PLACE_HINT_DOMAINS = ("buenourasoe.com",)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
OG_TITLE_RE = re.compile(
    r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']',
    re.IGNORECASE | re.DOTALL,
)
URL_RE = re.compile(r"https?://[^\s\])>]+")
TABLE_ROW_RE = re.compile(r"^\| (?P<name>.+?) \| (?P<area>.+?) \| (?P<kind>.+?) \| (?P<memo>.+?) \|$")
GENERIC_PREFIXES = (
    "福岡行ったら",
    "行くなら",
    "絶対次",
    "食べログ100名店",
)
GENERIC_SUFFIXES = (
    "土日ランチは2か月先くらいの予約 Tablecheckで",
    "候補",
)


@dataclass
class Candidate:
    section: str
    name: str
    area: str
    kind: str
    memo: str
    url: str
    source: str


def fetch_title(url: str) -> tuple[str | None, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            final_url = response.geturl()
            body = response.read(200_000)
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None, url

    text = body.decode("utf-8", errors="ignore")
    match = OG_TITLE_RE.search(text) or TITLE_RE.search(text)
    if not match:
        return None, final_url
    return html.unescape(match.group(1)).strip(), final_url


def canonicalize_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    if host.endswith("tabelog.com"):
        return f"https://tabelog.com{path}/"
    if host.endswith("x.com"):
        return f"https://x.com{path}"
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))


def normalize_name(name: str) -> str:
    normalized = name
    for prefix in GENERIC_PREFIXES:
        normalized = normalized.replace(prefix, "")
    for suffix in GENERIC_SUFFIXES:
        normalized = normalized.replace(suffix, "")
    normalized = normalized.replace("候補", "")
    normalized = re.sub(r"\s+", "", normalized)
    return normalized.strip().lower()


def classify_section(line: str, url: str) -> str:
    lowered = line.lower()
    host = urllib.parse.urlparse(url).netloc.lower()
    if "泊まりたい" in line:
        return "泊まりたい場所"
    if any(domain in host for domain in PLACE_HINT_DOMAINS) or "沖縄" in line:
        return "行ってみたい場所・旅行先"
    if "展" in line or "ミュージアム" in line:
        return "行きたいお店・展示"
    if any(domain in host for domain in FOOD_DOMAINS) or "食べたい" in line:
        return "行きたい飲食店"
    if "restaurant" in lowered or "ramen" in lowered:
        return "行きたい飲食店"
    return "行きたい飲食店"


def resolve_candidate(line: str, url: str, source: str, sequence: int) -> Candidate:
    title, final_url = fetch_title(url)
    final_url = canonicalize_url(final_url)
    host = urllib.parse.urlparse(final_url).netloc.lower()
    line_without_url = URL_RE.sub("", line).strip(" -。:：,[]()")

    name = ""
    area = "未整理"
    kind = "レストラン"

    if host.endswith("tabelog.com") and title:
        cleaned = re.sub(r"\s+\|\s+食べログ.*$", "", title).strip()
        matched = re.match(r"^(?P<name>.+?)\s*-\s*(?P<area>[^/|]+)(?:/(?P<genre>[^|]+))?$", cleaned)
        if matched:
            name = matched.group("name").strip()
            area = matched.group("area").strip()
            genre = (matched.group("genre") or "").strip()
            if genre:
                kind = genre
    elif host.endswith("ramendb.supleks.jp") and title:
        cleaned = re.sub(r"\s+\|\s+.*$", "", title).strip()
        matched = re.match(r"^(?P<name>.+?)\s*-\s*(?P<area>.+)$", cleaned)
        if matched:
            name = matched.group("name").strip()
            area = matched.group("area").strip()
            kind = "ラーメン"
    elif title:
        cleaned = re.sub(r"\s+\|\s+.*$", "", title).strip()
        cleaned = re.sub(r"\s+-\s+.*$", "", cleaned).strip()
        if cleaned:
            name = cleaned

    if not name:
        snippet = line_without_url
        for keyword in KEYWORDS:
            snippet = snippet.replace(keyword, "")
        for prefix in GENERIC_PREFIXES:
            snippet = snippet.replace(prefix, "")
        snippet = snippet.replace("Xのメモ起点", "").replace("行くなら", "")
        for suffix in GENERIC_SUFFIXES:
            snippet = snippet.replace(suffix, "")
        snippet = re.sub(r"[、。,:：\-\[\]]+", " ", snippet)
        snippet = " ".join(snippet.split()).strip()
        if snippet:
            name = snippet
        else:
            date_label = Path(source).stem
            name = f"{date_label}の候補 {sequence}"

    section = classify_section(line, final_url)
    if section == "泊まりたい場所":
        kind = "宿"
    elif section == "行ってみたい場所・旅行先":
        kind = "旅行先" if kind == "レストラン" else kind
    elif section == "行きたいお店・展示" and kind == "レストラン":
        kind = "店"

    memo_label = "URL自動取得"
    if "x.com" in host:
        memo_label = "Xメモ"
    elif host.endswith("tabelog.com"):
        memo_label = "食べログ"

    memo = f"[{memo_label}]({final_url})"
    return Candidate(section=section, name=name, area=area, kind=kind, memo=memo, url=final_url, source=source)


def parse_existing_urls(lines: list[str]) -> set[str]:
    urls: set[str] = set()
    for line in lines:
        for url in URL_RE.findall(line):
            urls.add(canonicalize_url(url.rstrip(").,")))
    return urls


def parse_existing_rows(lines: list[str]) -> tuple[dict[str, set[tuple[str, str]]], dict[str, set[str]]]:
    section = ""
    rows: dict[str, set[tuple[str, str]]] = {}
    names: dict[str, set[str]] = {}
    for raw_line in lines:
        line = raw_line.rstrip("\n")
        if line.startswith("## "):
            section = line[3:]
            rows.setdefault(section, set())
            names.setdefault(section, set())
            continue
        match = TABLE_ROW_RE.match(line)
        if match and section:
            name = match.group("name")
            rows.setdefault(section, set()).add((name, match.group("area")))
            names.setdefault(section, set()).add(normalize_name(name))
    return rows, names


def collect_diary_candidates(
    existing_urls: set[str],
    existing_rows: dict[str, set[tuple[str, str]]],
    existing_names: dict[str, set[str]],
) -> list[Candidate]:
    candidates: list[Candidate] = []
    for diary_path in sorted(DIARY_DIR.glob("*.md")):
        per_file_index = 0
        for line in diary_path.read_text().splitlines():
            if not any(keyword in line for keyword in KEYWORDS):
                continue
            urls = [url.rstrip(").,") for url in URL_RE.findall(line)]
            if not urls:
                continue
            for url in urls:
                if url in existing_urls:
                    continue
                per_file_index += 1
                candidate = resolve_candidate(line, url, str(diary_path), per_file_index)
                if candidate.url in existing_urls:
                    continue
                row_key = (candidate.name, candidate.area)
                normalized_name = normalize_name(candidate.name)
                if row_key in existing_rows.get(candidate.section, set()):
                    continue
                if normalized_name in existing_names.get(candidate.section, set()):
                    continue
                candidates.append(candidate)
                existing_urls.add(candidate.url)
                existing_rows.setdefault(candidate.section, set()).add(row_key)
                existing_names.setdefault(candidate.section, set()).add(normalized_name)
    return candidates


def insert_candidates(lines: list[str], section_name: str, candidates: list[Candidate]) -> list[str]:
    if not candidates:
        return lines

    start = None
    end = None
    for index, line in enumerate(lines):
        if line.startswith(f"## {section_name}"):
            start = index
            continue
        if start is not None and index > start and line.startswith("> [source:"):
            end = index
            break

    if start is None or end is None:
        return lines

    insert_at = end
    new_lines = [f"| {c.name} | {c.area} | {c.kind} | {c.memo} |\n" for c in candidates]
    return lines[:insert_at] + new_lines + lines[insert_at:]


def main() -> None:
    lines = PLACES_PATH.read_text().splitlines(keepends=True)
    existing_urls = parse_existing_urls(lines)
    existing_rows, existing_names = parse_existing_rows(lines)
    candidates = collect_diary_candidates(existing_urls, existing_rows, existing_names)

    by_section: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        by_section.setdefault(candidate.section, []).append(candidate)

    for section_name in (
        "行きたい飲食店",
        "行きたいお店・展示",
        "行ってみたい場所・旅行先",
        "泊まりたい場所",
    ):
        lines = insert_candidates(lines, section_name, by_section.get(section_name, []))

    PLACES_PATH.write_text("".join(lines))


if __name__ == "__main__":
    main()
