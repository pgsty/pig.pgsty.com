#!/usr/bin/env python3
"""Validate the bilingual PIG design-record contract."""

from __future__ import annotations

import pathlib
import re
import sys


DESIGN_DIR = pathlib.Path("content/blog/design")
ALLOWED_TAGS = {
    "repo",
    "ext",
    "postgres",
    "patroni",
    "pgbackrest",
    "pitr",
    "sty",
    "build",
    "inventory",
    "catalog",
    "cli",
    "install",
}
REQUIRED_KEYS = {
    "title",
    "linkTitle",
    "date",
    "lastmod",
    "description",
    "tags",
    "weight",
    "authors",
    "draft",
}
REQUIRED_ANCHORS = {
    "decision",
    "context",
    "alternatives",
    "contract",
    "impact",
    "verification",
    "status",
}
FORBIDDEN = {
    "local absolute path": re.compile(r"/Users/|/home/[A-Za-z0-9_.-]+/"),
    "retired local document reference": re.compile(r"docs/(?:spec|refactor)/"),
    "temporary review reference": re.compile(r"(?:^|[\s`/])tmp/"),
    "unfinished marker": re.compile(r"\b(?:TODO|TBD|DRAFT)\b"),
    "raw agent-review detail": re.compile(r"Claude Code|claude-(?:sonnet|opus|fable)", re.I),
}
ANCHOR_RE = re.compile(r"\{#([a-z0-9-]+)\}")


def parse_page(path: pathlib.Path) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, text, [f"{path}: missing YAML front matter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, text, [f"{path}: unclosed YAML front matter"]
    meta: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], 2):
        if not line or line.startswith((" ", "\t", "#")):
            continue
        if ":" not in line:
            errors.append(f"{path}:{number}: unsupported front matter line")
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, "\n".join(lines[end + 1 :]), errors


def parse_list(value: str) -> list[str]:
    if not (value.startswith("[") and value.endswith("]")):
        return []
    return [item.strip().strip("\"'") for item in value[1:-1].split(",") if item.strip()]


def validate_index(errors: list[str]) -> None:
    for name in ("_index.md", "_index.zh.md"):
        path = DESIGN_DIR / name
        if not path.is_file():
            errors.append(f"missing design index: {path}")
            continue
        meta, _, page_errors = parse_page(path)
        errors.extend(page_errors)
        for key in ("title", "linkTitle", "description", "weight", "module", "blog_index"):
            if not meta.get(key):
                errors.append(f"{path}: missing index front matter key {key}")


def validate_pair(english: pathlib.Path, chinese: pathlib.Path, errors: list[str]) -> None:
    en_meta, en_body, en_errors = parse_page(english)
    zh_meta, zh_body, zh_errors = parse_page(chinese)
    errors.extend(en_errors)
    errors.extend(zh_errors)

    for path, meta in ((english, en_meta), (chinese, zh_meta)):
        missing = sorted(REQUIRED_KEYS - meta.keys())
        if missing:
            errors.append(f"{path}: missing front matter keys: {', '.join(missing)}")
        if meta.get("authors") != "[Vonng]":
            errors.append(f"{path}: authors must be [Vonng]")
        if meta.get("draft") != "false":
            errors.append(f"{path}: draft must be false")
        tags = parse_list(meta.get("tags", ""))
        if not tags or len(tags) > 4:
            errors.append(f"{path}: tags must contain one to four entries")
        unknown = sorted(set(tags) - ALLOWED_TAGS)
        if unknown:
            errors.append(f"{path}: unknown tags: {', '.join(unknown)}")

    for key in ("date", "lastmod", "weight", "authors", "draft"):
        if en_meta.get(key) != zh_meta.get(key):
            errors.append(f"{english} / {chinese}: {key} differs")

    en_anchors = ANCHOR_RE.findall(en_body)
    zh_anchors = ANCHOR_RE.findall(zh_body)
    if set(en_anchors) != REQUIRED_ANCHORS:
        errors.append(f"{english}: design anchors differ from the required contract")
    if en_anchors != zh_anchors:
        errors.append(f"{english} / {chinese}: heading anchors or order differ")

    for path, body, marker in (
        (english, en_body, "**Decision date:**"),
        (chinese, zh_body, "**决策日期：**"),
    ):
        if marker not in body:
            errors.append(f"{path}: missing visible decision metadata")
        if "]( /" in body:
            errors.append(f"{path}: malformed internal link spacing")
        if "](/" not in body:
            errors.append(f"{path}: missing current-site reference")
        if "https://github.com/pgsty/pig/" not in body:
            errors.append(f"{path}: missing pinned source or release evidence")
        for label, pattern in FORBIDDEN.items():
            match = pattern.search(body)
            if match:
                errors.append(f"{path}: contains {label} near {match.group(0)!r}")


def main() -> int:
    errors: list[str] = []
    if not DESIGN_DIR.is_dir():
        print(f"missing design directory: {DESIGN_DIR}", file=sys.stderr)
        return 1

    validate_index(errors)
    english_pages = sorted(
        path
        for path in DESIGN_DIR.glob("*.md")
        if path.name != "_index.md" and not path.name.endswith(".zh.md")
    )
    if not english_pages:
        errors.append("design section has no English records")
    expected_chinese = {path.with_name(f"{path.stem}.zh.md") for path in english_pages}
    actual_chinese = {
        path for path in DESIGN_DIR.glob("*.zh.md") if path.name != "_index.zh.md"
    }
    for missing in sorted(expected_chinese - actual_chinese):
        errors.append(f"missing Chinese design record: {missing}")
    for orphan in sorted(actual_chinese - expected_chinese):
        errors.append(f"orphan Chinese design record: {orphan}")
    for english in english_pages:
        chinese = english.with_name(f"{english.stem}.zh.md")
        if chinese.is_file():
            validate_pair(english, chinese, errors)

    if errors:
        print(f"design check failed: {len(errors)} issues", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"design check passed: {len(english_pages)} bilingual records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
