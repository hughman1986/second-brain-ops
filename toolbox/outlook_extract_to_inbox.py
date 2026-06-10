"""Extract Outlook emails into a single Markdown note.

Usage examples::

    # Pull the last 7 days from default Inbox
    python toolbox/outlook_extract_to_inbox.py --since 2026-06-03 --slug weekly-review

    # Filter by sender + subject in a sub-folder
    python toolbox/outlook_extract_to_inbox.py \
        --folder "Inbox/Projects/CMP" --from "boss@company.com" --subject "review"

    # Fetch specific messages by EntryID and write to a project source/ folder
    python toolbox/outlook_extract_to_inbox.py --entry-id <ID1> --entry-id <ID2> \
        --slug pm-thread --out-dir 10_Projects/cmp-digital-twin/source

    # Dry run: just list matching messages
    python toolbox/outlook_extract_to_inbox.py --since 2026-06-01 --dry-run

Requires Windows + Office (Outlook) + the ``sb-docs`` venv with ``pywin32`` and
``html2text`` installed. The script never modifies Outlook items (no mark-as-
read, no move, no send).
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
INBOX_DIR = REPO_ROOT / "00_Inbox"
INBOX_INDEX = INBOX_DIR / "\u76ee\u9304.md"

OL_FOLDER_INBOX = 6  # olFolderInbox
OL_MAIL_ITEM = 43  # olMailItem


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract Outlook mail items into a combined Markdown note.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--folder",
        help='Outlook folder path, e.g. "Inbox/Projects/CMP". Defaults to the '
        "default Inbox of the chosen store.",
    )
    parser.add_argument(
        "--store",
        help="Outlook store / account display name (use when you have multiple "
        "mailboxes or PST files). Defaults to the default delivery store.",
    )
    parser.add_argument("--since", help="Only mails received on/after YYYY-MM-DD.")
    parser.add_argument("--until", help="Only mails received before YYYY-MM-DD (exclusive).")
    parser.add_argument(
        "--from",
        dest="from_filter",
        action="append",
        default=[],
        help="Filter by sender (substring match against name or email). Repeatable.",
    )
    parser.add_argument(
        "--subject",
        action="append",
        default=[],
        help="Filter by subject keyword (substring, case-insensitive). Repeatable.",
    )
    parser.add_argument(
        "--unread",
        action="store_true",
        help="Only include unread items.",
    )
    parser.add_argument(
        "--entry-id",
        action="append",
        default=[],
        help="Fetch specific mail by EntryID. Repeatable. Bypasses folder filters.",
    )
    parser.add_argument(
        "--conversation-id",
        help="Fetch all mails in a conversation (uses Application.AdvancedSearch).",
    )
    parser.add_argument("--limit", type=int, default=200, help="Max items (default 200).")
    parser.add_argument("--slug", help="Slug for filename + assets folder. Auto from subject if omitted.")
    parser.add_argument("--title", help="Note title. Defaults to first message subject.")
    parser.add_argument(
        "--out-dir",
        help="Output directory. Defaults to 00_Inbox/ (also updates Inbox index). "
        "Use a project's source/ folder to bypass the Inbox flow.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Capture date for filename + frontmatter. Defaults to today.",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Convert HTMLBody to Markdown via html2text (default uses plain Body).",
    )
    parser.add_argument(
        "--no-attachments",
        action="store_true",
        help="Skip saving attachments and inline images.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List matching messages and exit. No files written.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def slugify(text: str, fallback: str) -> str:
    lowered = (text or "").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if len(slug) < 4:
        slug = fallback
    return slug[:80].strip("-") or fallback


def yaml_quote(value: str) -> str:
    escaped = (value or "").replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def relative_to_repo(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d")


def safe_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name or "").strip().rstrip(".")
    return cleaned[:120] or "attachment"


# ---------------------------------------------------------------------------
# Outlook access
# ---------------------------------------------------------------------------


@dataclass
class MailRecord:
    entry_id: str
    conversation_id: str
    subject: str
    sender_name: str
    sender_email: str
    to: str
    cc: str
    received: datetime | None
    importance: int
    categories: str
    body_text: str
    body_html: str
    folder_path: str
    attachments: list[dict] = field(default_factory=list)


def connect_outlook():
    try:
        import win32com.client  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "pywin32 not available. Run inside the sb-docs venv: "
            "$env:USERPROFILE\\.venvs\\sb-docs\\Scripts\\python.exe"
        ) from exc
    app = win32com.client.Dispatch("Outlook.Application")
    return app, app.GetNamespace("MAPI")


def pick_store(namespace, store_name: str | None):
    if not store_name:
        return namespace.DefaultStore
    for store in namespace.Stores:
        if (store.DisplayName or "").lower() == store_name.lower():
            return store
    available = ", ".join(s.DisplayName for s in namespace.Stores)
    raise SystemExit(f"Store '{store_name}' not found. Available: {available}")


def resolve_folder(namespace, store, folder_path: str | None):
    if not folder_path:
        # Try default Inbox of the chosen store via EntryID hop; fall back to
        # the namespace default Inbox.
        try:
            default_inbox = namespace.GetDefaultFolder(OL_FOLDER_INBOX)
            if getattr(default_inbox.Store, "StoreID", None) == getattr(store, "StoreID", None):
                return default_inbox
        except Exception:
            pass
        try:
            return namespace.GetSharedDefaultFolder(store, OL_FOLDER_INBOX)
        except Exception:
            pass
        return namespace.GetDefaultFolder(OL_FOLDER_INBOX)

    parts = [p for p in re.split(r"[\\/]+", folder_path) if p]
    root = store.GetRootFolder()
    current = root
    # Try to descend from the store root; if first part doesn't match, also try
    # starting from the default Inbox (common UX shortcut).
    try:
        for part in parts:
            current = current.Folders.Item(part)
        return current
    except Exception:
        pass
    try:
        current = namespace.GetDefaultFolder(OL_FOLDER_INBOX)
        # If user wrote "Inbox/..." trim the first "Inbox".
        descend = parts[1:] if parts[0].lower() == "inbox" else parts
        for part in descend:
            current = current.Folders.Item(part)
        return current
    except Exception as exc:
        raise SystemExit(f"Folder '{folder_path}' not found in store '{store.DisplayName}': {exc}")


def folder_full_path(folder) -> str:
    try:
        return folder.FolderPath  # type: ignore[attr-defined]
    except Exception:
        return folder.Name


def to_datetime(value) -> datetime | None:
    if value is None:
        return None
    try:
        return datetime(
            value.year, value.month, value.day, value.hour, value.minute, value.second
        )
    except Exception:
        try:
            return datetime.fromisoformat(str(value))
        except Exception:
            return None


def iter_items_filtered(folder, *, since: datetime | None, until: datetime | None, limit: int):
    items = folder.Items
    try:
        items.Sort("[ReceivedTime]", True)
    except Exception:
        pass

    count = 0
    for item in items:
        if count >= limit:
            break
        try:
            if getattr(item, "Class", None) != OL_MAIL_ITEM:
                continue
            received = to_datetime(getattr(item, "ReceivedTime", None))
            if since and (received is None or received < since):
                continue
            if until and (received is None or received >= until):
                continue
        except Exception:
            continue
        yield item
        count += 1


def matches_filters(item, *, from_filters: list[str], subject_filters: list[str], unread: bool) -> bool:
    if unread and not getattr(item, "UnRead", False):
        return False
    if from_filters:
        sender_name = (getattr(item, "SenderName", "") or "").lower()
        sender_email = (getattr(item, "SenderEmailAddress", "") or "").lower()
        if not any(f.lower() in sender_name or f.lower() in sender_email for f in from_filters):
            return False
    if subject_filters:
        subject = (getattr(item, "Subject", "") or "").lower()
        if not any(s.lower() in subject for s in subject_filters):
            return False
    return True


def collect_by_entry_ids(namespace, entry_ids: list[str]) -> list:
    collected = []
    for eid in entry_ids:
        try:
            collected.append(namespace.GetItemFromID(eid))
        except Exception as exc:
            print(f"WARN: cannot load EntryID {eid[:20]}...: {exc}", file=sys.stderr)
    return collected


def collect_by_conversation(app, namespace, conversation_id: str, limit: int) -> list:
    # Walk through the default store's folders looking for items whose
    # ConversationID matches. Use AdvancedSearch for performance.
    scope = f"'{namespace.DefaultStore.GetRootFolder().FolderPath}'"
    filter_expr = f"urn:schemas:httpmail:thread-index IS NOT NULL"
    try:
        search = app.AdvancedSearch(Scope=scope, Filter=filter_expr, SearchSubFolders=True)
        # AdvancedSearch is async; for simplicity iterate the inbox conversation directly.
    except Exception:
        pass

    matches: list = []
    inbox = namespace.GetDefaultFolder(OL_FOLDER_INBOX)
    for item in inbox.Items:
        if len(matches) >= limit:
            break
        if getattr(item, "Class", None) != OL_MAIL_ITEM:
            continue
        if getattr(item, "ConversationID", None) == conversation_id:
            matches.append(item)
    return matches


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------


def html_to_markdown(html: str) -> str:
    if not html:
        return ""
    try:
        import html2text  # type: ignore
    except ImportError:
        return html
    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_links = False
    h.ignore_images = False
    h.protect_links = True
    return h.handle(html).strip()


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def save_attachments(item, out_dir: Path, index: int) -> list[dict]:
    saved: list[dict] = []
    try:
        attachments = item.Attachments
        count = attachments.Count
    except Exception:
        return saved
    if count == 0:
        return saved
    out_dir.mkdir(parents=True, exist_ok=True)
    for n in range(1, count + 1):
        att = attachments.Item(n)
        fname = safe_filename(getattr(att, "FileName", f"attachment-{n}"))
        target = out_dir / f"mail{index:02d}_{n:02d}_{fname}"
        try:
            att.SaveAsFile(str(target))
        except Exception as exc:
            print(f"WARN: cannot save attachment {fname}: {exc}", file=sys.stderr)
            continue
        saved.append({"name": fname, "path": target})
    return saved


def item_to_record(item, *, want_html: bool, save_atts: bool, asset_dir: Path, index: int) -> MailRecord:
    received = to_datetime(getattr(item, "ReceivedTime", None))
    folder_name = ""
    try:
        folder_name = item.Parent.FolderPath  # type: ignore[attr-defined]
    except Exception:
        try:
            folder_name = item.Parent.Name
        except Exception:
            pass

    body_text = clean_text(getattr(item, "Body", "") or "")
    body_html = ""
    if want_html:
        body_html = getattr(item, "HTMLBody", "") or ""

    attachments: list[dict] = []
    if save_atts:
        attachments = save_attachments(item, asset_dir, index)

    return MailRecord(
        entry_id=getattr(item, "EntryID", "") or "",
        conversation_id=getattr(item, "ConversationID", "") or "",
        subject=(getattr(item, "Subject", "") or "(no subject)").strip(),
        sender_name=getattr(item, "SenderName", "") or "",
        sender_email=getattr(item, "SenderEmailAddress", "") or "",
        to=getattr(item, "To", "") or "",
        cc=getattr(item, "CC", "") or "",
        received=received,
        importance=getattr(item, "Importance", 1) or 1,
        categories=getattr(item, "Categories", "") or "",
        body_text=body_text,
        body_html=body_html,
        folder_path=folder_name,
        attachments=attachments,
    )


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------


IMPORTANCE_LABEL = {0: "Low", 1: "Normal", 2: "High"}


def format_dt(dt: datetime | None) -> str:
    return dt.strftime("%Y-%m-%d %H:%M") if dt else "unknown"


def build_markdown(
    *,
    title: str,
    slug: str,
    source_label: str,
    created: str,
    records: list[MailRecord],
    out_dir: Path,
    use_html: bool,
) -> str:
    senders = sorted({r.sender_name or r.sender_email for r in records if (r.sender_name or r.sender_email)})
    dates = [r.received for r in records if r.received]
    date_range = "\u2014"
    if dates:
        date_range = f"{format_dt(min(dates))} ~ {format_dt(max(dates))}"
    body_mode_label = "HTML \u2192 markdown" if use_html else "plain text"
    senders_label = ", ".join(senders) if senders else "\u2014"

    lines: list[str] = [
        "---",
        f"title: {yaml_quote(title)}",
        f"source: {yaml_quote(source_label)}",
        f"created: {created}",
        f"updated: {created}",
        "para: inbox",
        "tags: [mail, outlook, raw-extract, needs-review]",
        "status: captured",
        "extraction_type: raw-outlook",
        f"mail_count: {len(records)}",
        "---",
        "",
        f"# {title}",
        "",
        "## Source",
        "",
        f"- Outlook source: {source_label}",
        f"- Mail count: {len(records)}",
        f"- Captured: {created}",
        f"- Body mode: {body_mode_label}",
        "",
        "## Thread Summary",
        "",
        f"- Date range: {date_range}",
        f"- Senders: {senders_label}",
        "",
        "## Mails",
        "",
    ]

    for idx, rec in enumerate(records, start=1):
        header = f"### {idx:02d}. {rec.subject} \u2014 {rec.sender_name or rec.sender_email} ({format_dt(rec.received)})"
        lines.append(header)
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("| --- | --- |")
        lines.append(f"| From | {rec.sender_name} <{rec.sender_email}> |")
        lines.append(f"| To | {rec.to} |")
        if rec.cc:
            lines.append(f"| Cc | {rec.cc} |")
        lines.append(f"| Received | {format_dt(rec.received)} |")
        lines.append(f"| Folder | {rec.folder_path} |")
        lines.append(f"| Importance | {IMPORTANCE_LABEL.get(rec.importance, rec.importance)} |")
        if rec.categories:
            lines.append(f"| Categories | {rec.categories} |")
        lines.append(f"| EntryID | `{rec.entry_id}` |")
        if rec.conversation_id:
            lines.append(f"| ConversationID | `{rec.conversation_id}` |")
        lines.append("")

        if rec.attachments:
            lines.append("**Attachments**")
            lines.append("")
            for att in rec.attachments:
                try:
                    rel = att["path"].resolve().relative_to(out_dir.resolve()).as_posix()
                except ValueError:
                    rel = att["path"].as_posix()
                lines.append(f"- [{att['name']}]({rel})")
            lines.append("")

        lines.append("**Body**")
        lines.append("")
        if use_html and rec.body_html:
            md = html_to_markdown(rec.body_html)
            lines.append(md if md else "_empty body_")
        else:
            text = rec.body_text or "_empty body_"
            lines.append("```text")
            lines.append(text)
            lines.append("```")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Inbox index update (only when writing to 00_Inbox)
# ---------------------------------------------------------------------------


def upsert_inbox_index(*, note_path: Path, title: str, updated: str, mail_count: int) -> None:
    if not INBOX_INDEX.exists():
        raise FileNotFoundError(f"Missing inbox index: {INBOX_INDEX}")

    index = INBOX_INDEX.read_text(encoding="utf-8")
    link = note_path.name.replace(" ", "%20")
    summary = (
        f"Outlook \u539f\u59cb\u62bd\u53d6\u6a94\uff0c\u5408\u4f75 {mail_count} "
        f"\u5c01\u4fe1\u4ef6\u3002\u5c1a\u672a\u4f9d CODE/PARA \u8403\u53d6\u6574\u7406\u3002"
    )
    row = (
        f"| [{title}]({link}) | captured / needs-review | {summary} | {updated} | "
        f"\u53ef\u8403\u53d6\u70ba\u6703\u8b70\u7d00\u9304\u3001\u6c7a\u7b56\u7d00\u9304\u3001"
        f"\u5c08\u6848\u9032\u5ea6\u6216 SOP\u3002 |"
    )

    lines = index.splitlines()
    filtered = [
        line
        for line in lines
        if note_path.name not in line and "_\u5c1a\u7121\u7b46\u8a18_" not in line and title not in line
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def collect_items(args, app, namespace) -> tuple[list, str]:
    if args.entry_id:
        items = collect_by_entry_ids(namespace, args.entry_id)
        return items, f"outlook://entry-id ({len(items)} items)"

    if args.conversation_id:
        items = collect_by_conversation(app, namespace, args.conversation_id, args.limit)
        return items, f"outlook://conversation/{args.conversation_id}"

    store = pick_store(namespace, args.store)
    folder = resolve_folder(namespace, store, args.folder)
    since = parse_date(args.since)
    until = parse_date(args.until)

    matched = []
    for item in iter_items_filtered(folder, since=since, until=until, limit=args.limit * 4):
        if matches_filters(
            item,
            from_filters=args.from_filter,
            subject_filters=args.subject,
            unread=args.unread,
        ):
            matched.append(item)
        if len(matched) >= args.limit:
            break

    label = f"outlook://{store.DisplayName}/{folder_full_path(folder)}"
    return matched, label


def main() -> int:
    args = parse_args()
    try:
        app, namespace = connect_outlook()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"ERROR: cannot connect to Outlook: {exc}", file=sys.stderr)
        return 1

    try:
        items, source_label = collect_items(args, app, namespace)
    except SystemExit:
        raise
    except Exception as exc:
        print(f"ERROR: cannot collect items: {exc}", file=sys.stderr)
        return 1

    if not items:
        print("No mails matched the given filters.", file=sys.stderr)
        return 2

    # Order chronologically (oldest first) for thread readability.
    items_sorted = sorted(items, key=lambda i: to_datetime(getattr(i, "ReceivedTime", None)) or datetime.min)

    if args.dry_run:
        print(f"Matched {len(items_sorted)} mail(s) from {source_label}:")
        for idx, item in enumerate(items_sorted, start=1):
            subj = (getattr(item, "Subject", "") or "(no subject)").strip()
            sender = getattr(item, "SenderName", "") or getattr(item, "SenderEmailAddress", "")
            received = format_dt(to_datetime(getattr(item, "ReceivedTime", None)))
            print(f"  {idx:02d}. [{received}] {sender} | {subj}")
        return 0

    first_subject = (getattr(items_sorted[0], "Subject", "") or "outlook-thread").strip()
    title = args.title or f"{first_subject} (Outlook \u8a0a\u606f\u4e32)"
    slug = slugify(args.slug or first_subject, "outlook-thread")

    out_dir = Path(args.out_dir).resolve() if args.out_dir else INBOX_DIR
    if not out_dir.is_absolute():
        out_dir = (REPO_ROOT / out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    asset_dir = out_dir / "assets" / slug
    if asset_dir.exists() and not args.no_attachments:
        shutil.rmtree(asset_dir)

    records: list[MailRecord] = []
    for idx, item in enumerate(items_sorted, start=1):
        record = item_to_record(
            item,
            want_html=args.html,
            save_atts=not args.no_attachments,
            asset_dir=asset_dir,
            index=idx,
        )
        records.append(record)

    note_name = f"{args.date} - {slug}-mail.md"
    note_path = out_dir / note_name

    markdown = build_markdown(
        title=title,
        slug=slug,
        source_label=source_label,
        created=args.date,
        records=records,
        out_dir=out_dir,
        use_html=args.html,
    )
    note_path.write_text(markdown, encoding="utf-8")

    inbox_updated = False
    if out_dir.resolve() == INBOX_DIR.resolve():
        try:
            upsert_inbox_index(
                note_path=note_path,
                title=title,
                updated=args.date,
                mail_count=len(records),
            )
            inbox_updated = True
        except Exception as exc:
            print(f"WARN: failed to update 00_Inbox/\u76ee\u9304.md: {exc}", file=sys.stderr)

    try:
        rel = note_path.relative_to(REPO_ROOT)
    except ValueError:
        rel = note_path
    print(f"Wrote: {rel}")
    print(f"Mails: {len(records)}")
    total_attachments = sum(len(r.attachments) for r in records)
    print(f"Attachments: {total_attachments}")
    if inbox_updated:
        print("Updated: 00_Inbox/\u76ee\u9304.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
