"""Extract PDF text and embedded images into a Markdown inbox note.

Usage:
    python toolbox/pdf_extract_to_inbox.py "<pdf-path>"
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import fitz  # PyMuPDF


REPO_ROOT = Path(__file__).resolve().parents[1]
INBOX_DIR = REPO_ROOT / "00_Inbox"
ASSETS_DIR = INBOX_DIR / "assets"
INBOX_INDEX = INBOX_DIR / "\u76ee\u9304.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract raw text and embedded images from a PDF into 00_Inbox."
    )
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Capture date in YYYY-MM-DD format. Defaults to today.",
    )
    return parser.parse_args()


def resolve_pdf_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file: {path}")
    return path


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


def relative_to_repo(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def relative_to_inbox(path: Path) -> str:
    try:
        return path.resolve().relative_to(INBOX_DIR).as_posix()
    except ValueError:
        return relative_to_repo(path)


def find_existing_note_by_source(source_path: str) -> Path | None:
    if not INBOX_DIR.exists():
        return None
    needles = {f"source: {source_path}", f"source: {yaml_quote(source_path)}"}
    for path in sorted(INBOX_DIR.glob("*.md")):
        if path.name == "\u76ee\u9304.md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(needle in text for needle in needles):
            return path
    return None


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def image_extension(image_info: dict) -> str:
    ext = str(image_info.get("ext") or "png").lower()
    if ext == "jpeg":
        ext = "jpg"
    if not re.fullmatch(r"[a-z0-9]+", ext):
        ext = "png"
    return ext


def extract_pdf(pdf_path: Path, asset_slug: str) -> tuple[dict, list[dict], list[dict]]:
    doc = fitz.open(pdf_path)
    metadata = doc.metadata or {}
    asset_dir = ASSETS_DIR / asset_slug
    if asset_dir.exists():
        shutil.rmtree(asset_dir)
    asset_dir.mkdir(parents=True, exist_ok=True)

    pages: list[dict] = []
    images: list[dict] = []

    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        text = clean_text(page.get_text("text"))
        page_images = page.get_images(full=True)
        page_image_paths: list[str] = []

        for image_index, image in enumerate(page_images, start=1):
            xref = image[0]
            try:
                extracted = doc.extract_image(xref)
            except Exception:
                continue
            ext = image_extension(extracted)
            filename = f"page-{page_index + 1:03d}-image-{image_index:02d}.{ext}"
            out_path = asset_dir / filename
            out_path.write_bytes(extracted["image"])
            rel_path = relative_to_inbox(out_path)
            page_image_paths.append(rel_path)
            images.append(
                {
                    "page": page_index + 1,
                    "path": rel_path,
                    "width": extracted.get("width"),
                    "height": extracted.get("height"),
                    "ext": ext,
                }
            )

        pages.append(
            {
                "number": page_index + 1,
                "text": text,
                "char_count": len(text),
                "images": page_image_paths,
            }
        )

    doc.close()
    return metadata, pages, images


def build_markdown(
    *,
    title: str,
    source_path: str,
    created: str,
    metadata: dict,
    pages: list[dict],
    images: list[dict],
) -> str:
    lines = [
        "---",
        f"title: {yaml_quote(title + ' PDF raw extract')}",
        f"source: {source_path}",
        f"created: {created}",
        f"updated: {created}",
        "para: inbox",
        "tags: [pdf, raw-extract, needs-review]",
        "status: captured",
        "extraction_type: raw-pdf",
        "---",
        "",
        f"# {title} PDF raw extract",
        "",
        "## Source",
        "",
        f"- PDF: {source_path}",
        f"- Pages: {len(pages)}",
        f"- Extracted images: {len(images)}",
        f"- Captured: {created}",
        "",
        "## Extraction Summary",
        "",
        "- \u9019\u662f PDF \u539f\u59cb\u62bd\u53d6\u6a94\uff0c\u5c1a\u672a\u4f9d CODE/PARA \u8403\u53d6\u6574\u7406\u3002",
        "- \u672c\u5de5\u5177\u53ea\u62bd\u53d6\u9801\u9762\u6587\u5b57\u8207\u5167\u5d4c\u5716\u7247\uff0c\u4e0d\u505a OCR \u6216 AI \u8996\u89ba\u89e3\u8b80\u3002",
        "",
        "## PDF Metadata",
        "",
    ]

    visible_metadata = {
        key: value
        for key, value in metadata.items()
        if value not in (None, "") and key not in {"format"}
    }
    if visible_metadata:
        for key in sorted(visible_metadata):
            lines.append(f"- {key}: {visible_metadata[key]}")
    else:
        lines.append("- _No metadata extracted._")

    lines += ["", "## Images", ""]
    if images:
        for item in images:
            lines.append(
                f"- Page {item['page']}: [{Path(item['path']).name}]({item['path']}) "
                f"({item.get('width')}x{item.get('height')}, {item.get('ext')})"
            )
    else:
        lines.append("- _No embedded images extracted._")

    lines += ["", "## Page Text", ""]
    for page in pages:
        lines.append(f"### Page {page['number']}")
        lines.append("")
        if page["images"]:
            lines.append("Images on this page:")
            for image_path in page["images"]:
                lines.append(f"- [{Path(image_path).name}]({image_path})")
            lines.append("")
        text = page["text"]
        if text:
            lines.append("```text")
            lines.append(text)
            lines.append("```")
        else:
            lines.append("_No selectable text extracted from this page._")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def upsert_inbox_index(
    *,
    note_path: Path,
    title: str,
    updated: str,
    page_count: int,
    image_count: int,
) -> None:
    if not INBOX_INDEX.exists():
        raise FileNotFoundError(f"Missing inbox index: {INBOX_INDEX}")

    index = INBOX_INDEX.read_text(encoding="utf-8")
    link = note_path.name.replace(" ", "%20")
    row = (
        f"| [{title} PDF raw extract]({link}) | captured / needs-review | "
        f"PDF \u539f\u59cb\u62bd\u53d6\u6a94\uff0c\u542b {page_count} \u9801\u6587\u5b57\u8207 "
        f"{image_count} \u500b\u5167\u5d4c\u5716\u7247\u7d22\u5f15\u3002\u5c1a\u672a\u4f9d CODE/PARA \u8403\u53d6\u6574\u7406\u3002 | "
        f"{updated} | \u53ef\u6574\u7406\u6210\u6587\u4ef6\u6458\u8981\u3001\u7814\u7a76\u7b46\u8a18\u6216\u8f38\u51fa\u7d20\u6750\u3002 |"
    )

    lines = index.splitlines()
    filtered = [
        line
        for line in lines
        if note_path.name not in line
        and "_\u5c1a\u7121\u7b46\u8a18_" not in line
        and f"{title} PDF raw extract" not in line
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
    try:
        pdf_path = resolve_pdf_path(args.pdf_path)
        source_path = relative_to_repo(pdf_path)
        title = pdf_path.stem
        slug = slugify(title, "pdf-document")
        existing = find_existing_note_by_source(source_path)
        out_path = existing or (INBOX_DIR / f"{args.date} - {slug}-extract.md")
        metadata, pages, images = extract_pdf(pdf_path, slug)
        markdown = build_markdown(
            title=title,
            source_path=source_path,
            created=args.date,
            metadata=metadata,
            pages=pages,
            images=images,
        )
        INBOX_DIR.mkdir(exist_ok=True)
        out_path.write_text(markdown, encoding="utf-8")
        upsert_inbox_index(
            note_path=out_path,
            title=title,
            updated=args.date,
            page_count=len(pages),
            image_count=len(images),
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote: {out_path.relative_to(REPO_ROOT)}")
    print(f"Pages: {len(pages)}")
    print(f"Images: {len(images)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
