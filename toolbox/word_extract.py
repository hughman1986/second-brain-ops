"""Extract Word (.docx / .doc) text, headings, tables, images to markdown.

Usage:
    python toolbox/word_extract.py <src.docx|src.doc> <out_dir>

Outputs:
    <out_dir>/<stem>_extract.md
    <out_dir>/assets/<stem>/imgN.<ext>

Behaviour:
    .docx -> parsed directly with python-docx (cross-platform, lossless markdown).
    .doc  -> converted to temp .docx via Word COM (Windows + Office required),
             then parsed the same way.

Headers/footers are skipped to avoid repeated page artefacts.
This tool only does raw extraction; no AI summarisation, no OCR.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn


def convert_doc_to_docx(src: Path) -> Path:
    """Use Word COM to convert legacy .doc to .docx into a temp file."""
    try:
        import win32com.client  # type: ignore
    except ImportError as e:
        raise SystemExit(
            "pywin32 required for .doc conversion. Run:\n"
            "  & 'C:\\Users\\jmhuang\\.venvs\\sb-docs\\Scripts\\python.exe' -m pip install pywin32"
        ) from e

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".docx")
    os.close(tmp_fd)
    tmp = Path(tmp_path)
    tmp.unlink(missing_ok=True)  # Word needs the path free
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(str(src.resolve()), ReadOnly=True)
        # wdFormatXMLDocument = 12 (.docx)
        doc.SaveAs(str(tmp.resolve()), FileFormat=12)
        doc.Close(SaveChanges=False)
    finally:
        word.Quit()
    return tmp


def iter_block_items(parent):
    """Yield paragraphs and tables in document order."""
    from docx.document import Document as _Doc
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table, _Cell
    from docx.text.paragraph import Paragraph

    if isinstance(parent, _Doc):
        elem = parent.element.body
    elif isinstance(parent, _Cell):
        elem = parent._tc
    else:
        elem = parent

    for child in elem.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def heading_level(paragraph) -> int:
    """Return 1..6 if paragraph style is a heading, else 0."""
    name = (paragraph.style.name or "").strip()
    if name.lower().startswith("heading "):
        try:
            n = int(name.split()[-1])
            return max(1, min(6, n))
        except ValueError:
            return 0
    if name in ("Title",):
        return 1
    return 0


def render_table(table) -> list[str]:
    rows = []
    for row in table.rows:
        cells = []
        seen_tc_ids = []
        for cell in row.cells:
            # python-docx returns the same underlying <w:tc> for cells merged
            # horizontally (gridSpan) or vertically (vMerge). Skip duplicates so
            # merged-cell content isn't repeated N times.
            tc_id = id(cell._tc)
            if tc_id in seen_tc_ids:
                continue
            seen_tc_ids.append(tc_id)
            text = " / ".join(
                p.text.strip() for p in cell.paragraphs if p.text.strip()
            )
            cells.append(text.replace("|", "\\|"))
        if not cells:
            continue
        rows.append("| " + " | ".join(cells) + " |")
    if not rows:
        return []
    # Use the widest row's column count for the separator so markdown stays valid
    col_count = max(r.count("|") - 1 for r in rows)
    sep = "| " + " | ".join(["---"] * col_count) + " |"
    return [rows[0], sep, *rows[1:], ""]


def extract_images(doc: Document, assets_dir: Path) -> dict[str, Path]:
    """Save embedded images. Returns rId -> saved path map."""
    assets_dir.mkdir(parents=True, exist_ok=True)
    saved: dict[str, Path] = {}
    rels = doc.part.rels
    idx = 0
    for rel_id, rel in rels.items():
        if "image" in rel.reltype:
            idx += 1
            blob = rel.target_part.blob
            ext = Path(rel.target_ref).suffix or ".bin"
            out = assets_dir / f"img{idx}{ext}"
            out.write_bytes(blob)
            saved[rel_id] = out
    return saved


def paragraph_images(paragraph) -> list[str]:
    """Return list of rIds for images embedded inline in this paragraph."""
    rids = []
    for blip in paragraph._element.iter(qn("a:blip")):
        rid = blip.get(qn("r:embed")) or blip.get(qn("r:link"))
        if rid:
            rids.append(rid)
    return rids


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)

    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    if not src.exists():
        sys.exit(f"source not found: {src}")
    out_dir.mkdir(parents=True, exist_ok=True)

    tmp_to_clean = None
    ext = src.suffix.lower()
    if ext == ".doc":
        print(f"[word_extract] .doc detected; converting via Word COM...")
        docx_path = convert_doc_to_docx(src)
        tmp_to_clean = docx_path
    elif ext == ".docx":
        docx_path = src
    else:
        sys.exit(f"unsupported extension: {ext} (expect .doc or .docx)")

    doc = Document(str(docx_path))
    assets_dir = out_dir / "assets" / src.stem
    images = extract_images(doc, assets_dir)

    lines: list[str] = [
        f"# {src.stem} (Word extract)",
        "",
        f"- source: `{src.name}`",
        f"- extracted_with: word_extract.py ({'docx' if ext == '.docx' else 'doc via Word COM'})",
        f"- images: {len(images)} (saved to `{assets_dir.relative_to(out_dir) if assets_dir.is_relative_to(out_dir) else assets_dir}/`)",
        "",
        "---",
        "",
    ]

    from docx.table import Table
    from docx.text.paragraph import Paragraph

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text.rstrip()
            lvl = heading_level(block)
            img_rids = paragraph_images(block)
            for rid in img_rids:
                if rid in images:
                    rel = images[rid].relative_to(out_dir).as_posix()
                    lines.append(f"![{images[rid].name}]({rel})")
            if not text:
                if not img_rids:
                    lines.append("")
                continue
            if lvl:
                lines.append("")
                lines.append(f"{'#' * (lvl + 1)} {text}")
                lines.append("")
            else:
                lines.append(text)
        elif isinstance(block, Table):
            lines.append("")
            lines.extend(render_table(block))

    out_md = out_dir / f"{src.stem}_extract.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"[word_extract] wrote {out_md}")
    print(f"[word_extract] images: {len(images)} in {assets_dir}")

    if tmp_to_clean and tmp_to_clean.exists():
        try:
            tmp_to_clean.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    main()
