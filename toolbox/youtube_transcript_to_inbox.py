"""Capture a YouTube transcript as a Markdown inbox note.

Usage:
    python toolbox/youtube_transcript_to_inbox.py "<youtube-url>"
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import date
from pathlib import Path
from typing import Iterable

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)


LANGUAGE_PRIORITY = ["zh-TW", "zh-Hant", "zh", "en"]
REPO_ROOT = Path(__file__).resolve().parents[1]
INBOX_DIR = REPO_ROOT / "00_Inbox"
INBOX_INDEX = INBOX_DIR / "\u76ee\u9304.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download public YouTube captions into 00_Inbox as Markdown."
    )
    parser.add_argument("url", help="YouTube URL or video id")
    parser.add_argument(
        "--languages",
        default=",".join(LANGUAGE_PRIORITY),
        help="Comma-separated transcript language priority list.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Capture date in YYYY-MM-DD format. Defaults to today.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=True,
        help="Overwrite an existing note with the same source URL. Enabled by default.",
    )
    return parser.parse_args()


def extract_video_id(value: str) -> str:
    value = value.strip()
    patterns = [
        r"(?:youtube\.com/watch\?.*?v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    raise ValueError(f"Cannot parse YouTube video id from: {value}")


def fetch_metadata(url: str) -> dict[str, object]:
    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        return ydl.extract_info(url, download=False)


def select_transcript(video_id: str, languages: list[str]):
    transcript_list = YouTubeTranscriptApi().list(video_id)
    selectors = [
        transcript_list.find_manually_created_transcript,
        transcript_list.find_generated_transcript,
        transcript_list.find_transcript,
    ]
    last_error: Exception | None = None
    for selector in selectors:
        try:
            transcript = selector(languages)
            return transcript, transcript.fetch()
        except Exception as exc:  # library exposes several selection errors
            last_error = exc
    if last_error:
        raise last_error
    raise NoTranscriptFound(video_id, languages, transcript_list)


def timestamp(seconds: float) -> str:
    total = int(seconds)
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def slugify(text: str, fallback: str) -> str:
    lowered = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if len(slug) < 4:
        slug = fallback
    return slug[:80].strip("-")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def find_existing_note_by_source(source_url: str) -> Path | None:
    if not INBOX_DIR.exists():
        return None
    for path in sorted(INBOX_DIR.glob("*.md")):
        if path.name == "\u76ee\u9304.md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if f"source: {source_url}" in text or f"source: {yaml_quote(source_url)}" in text:
            return path
    return None


def build_markdown(
    *,
    title: str,
    source_url: str,
    channel: str,
    created: str,
    language_code: str,
    is_generated: bool,
    snippets: Iterable[object],
) -> str:
    transcript_type = "auto-generated" if is_generated else "manual"
    lines = [
        "---",
        f"title: {yaml_quote(title + ' \u9010\u5b57\u7a3f')}",
        f"source: {source_url}",
        f"channel: {yaml_quote(channel)}",
        f"created: {created}",
        f"updated: {created}",
        "para: inbox",
        "tags: [youtube, transcript, needs-review]",
        "status: captured",
        f"language: {language_code}",
        f"transcript_type: {transcript_type}",
        "---",
        "",
        f"# {title} \u9010\u5b57\u7a3f",
        "",
        "## Source",
        "",
        f"- URL: {source_url}",
        f"- Channel: {channel}",
        f"- Transcript language: {language_code}",
        f"- Transcript type: {transcript_type}",
        f"- Captured: {created}",
        "",
        "## Notes",
        "",
        "- \u9019\u662f YouTube \u5b57\u5e55\u9010\u5b57\u7a3f\uff0c\u5c1a\u672a\u4f9d CODE/PARA \u8403\u53d6\u6574\u7406\u3002",
        "- \u4e0b\u4e00\u6b65\u53ef\u6574\u7406\u6210 Summary\u3001Key Ideas\u3001Distilled Points\u3001Action Items\u3001Possible Outputs\u3002",
        "",
        "## Transcript",
        "",
    ]
    for item in snippets:
        text = html.unescape(item.text).replace("\n", " ").strip()
        lines.append(f"[{timestamp(item.start)}] {text}")
    return "\n".join(lines) + "\n"


def upsert_inbox_index(
    *,
    note_path: Path,
    title: str,
    channel: str,
    updated: str,
) -> None:
    if not INBOX_INDEX.exists():
        raise FileNotFoundError(f"Missing inbox index: {INBOX_INDEX}")

    index = INBOX_INDEX.read_text(encoding="utf-8")
    link = note_path.name.replace(" ", "%20")
    row = (
        f"| [{title} \u9010\u5b57\u7a3f]({link}) | captured / needs-review | "
        f"YouTube \u5f71\u7247\u5b57\u5e55\u9010\u5b57\u7a3f\uff0c\u983b\u9053\u70ba {channel}\u3002"
        f"\u5c1a\u672a\u4f9d CODE/PARA \u8403\u53d6\u6574\u7406\u3002 | {updated} | "
        "\u53ef\u6574\u7406\u6210\u4e3b\u984c\u7b46\u8a18\u3001\u5b78\u7fd2\u7b46\u8a18\u6216\u8f38\u51fa\u7d20\u6750\u3002 |"
    )

    lines = index.splitlines()
    filtered = [
        line
        for line in lines
        if note_path.name not in line
        and "_\u5c1a\u7121\u7b46\u8a18_" not in line
        and title not in line
    ]

    insert_at = None
    for i, line in enumerate(filtered):
        if line.startswith("| --- "):
            insert_at = i + 1
            break
    if insert_at is None:
        raise ValueError("Cannot find markdown table separator in 00_Inbox/\u76ee\u9304.md")

    filtered.insert(insert_at, row)
    INBOX_INDEX.write_text("\n".join(filtered) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    languages = [item.strip() for item in args.languages.split(",") if item.strip()]

    try:
        video_id = extract_video_id(args.url)
        metadata = fetch_metadata(args.url)
        source_url = str(metadata.get("webpage_url") or f"https://www.youtube.com/watch?v={video_id}")
        title = str(metadata.get("title") or video_id)
        channel = str(metadata.get("channel") or metadata.get("uploader") or "unknown")
        transcript, snippets = select_transcript(video_id, languages)
    except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: failed to capture transcript: {exc}", file=sys.stderr)
        return 1

    INBOX_DIR.mkdir(exist_ok=True)
    existing = find_existing_note_by_source(source_url)
    if existing:
        out_path = existing
    else:
        filename = f"{args.date} - {slugify(title, video_id)}-transcript.md"
        out_path = INBOX_DIR / filename

    language_code = getattr(transcript, "language_code", languages[0])
    is_generated = bool(getattr(transcript, "is_generated", False))
    markdown = build_markdown(
        title=title,
        source_url=source_url,
        channel=channel,
        created=args.date,
        language_code=language_code,
        is_generated=is_generated,
        snippets=snippets,
    )
    out_path.write_text(markdown, encoding="utf-8")
    upsert_inbox_index(
        note_path=out_path,
        title=title,
        channel=channel,
        updated=args.date,
    )

    print(f"Wrote: {out_path.relative_to(REPO_ROOT)}")
    print(f"Transcript snippets: {len(snippets)}")
    print(f"Language: {language_code}")
    print(f"Generated: {is_generated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

