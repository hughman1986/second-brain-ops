"""Scan active equipment work orders for due reminders.

Usage:
    python toolbox/project_reminder_scan.py
    python toolbox/project_reminder_scan.py --date 2026-05-23 --days 7
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = REPO_ROOT / "10_Projects"
DONE_STATUSES = {"done", "closed", "cancelled", "canceled", "skipped"}


@dataclass
class Reminder:
    machine_model: str
    work_order: str
    source: str
    kind: str
    item: str
    status: str
    owner: str
    due_date: date | None
    remind_on: date | None
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan 10_Projects recursively for due schedule and issue reminders."
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Reference date in YYYY-MM-DD format. Defaults to today.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Look ahead this many days for reminders. Defaults to 7.",
    )
    return parser.parse_args()


def parse_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return all(cell.replace("-", "").replace(":", "").strip() == "" for cell in cells)


def read_markdown_tables(path: Path) -> list[list[dict[str, str]]]:
    if not path.exists():
        return []

    tables: list[list[dict[str, str]]] = []
    current_header: list[str] | None = None
    current_rows: list[dict[str, str]] = []

    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            if current_header and current_rows:
                tables.append(current_rows)
            current_header = None
            current_rows = []
            continue

        cells = split_row(line)
        if is_separator(cells):
            continue

        if current_header is None:
            current_header = cells
            current_rows = []
            continue

        row = {header: cells[index] if index < len(cells) else "" for index, header in enumerate(current_header)}
        current_rows.append(row)

    if current_header and current_rows:
        tables.append(current_rows)

    return tables


def project_context(path: Path) -> tuple[str, str]:
    """Return machine model and work order for a schedule/issues file.

    Preferred structure:
        10_Projects/<machine-model>/<work-order-id>/schedule.md

    Legacy structure is still supported:
        10_Projects/<project-slug>/schedule.md
    """

    relative_parts = path.relative_to(PROJECTS_DIR).parts
    parent_parts = relative_parts[:-1]
    if len(parent_parts) >= 2:
        return parent_parts[0], parent_parts[-1]
    if len(parent_parts) == 1:
        return "", parent_parts[0]
    return "", ""


def should_report(
    status: str,
    target_date: date | None,
    remind_on: date | None,
    today: date,
    horizon: date,
) -> tuple[bool, str]:
    normalized_status = status.strip().lower()
    if normalized_status in DONE_STATUSES:
        return False, ""

    if target_date and target_date < today:
        return True, "overdue"
    if remind_on and remind_on <= today:
        return True, "due-reminder"
    if remind_on and remind_on <= horizon:
        return True, "upcoming-reminder"
    if target_date and target_date <= horizon:
        return True, "upcoming-target"
    return False, ""


def scan_schedule(path: Path, today: date, horizon: date) -> list[Reminder]:
    reminders: list[Reminder] = []
    machine_model, work_order = project_context(path)
    for table in read_markdown_tables(path):
        if not table or "Stage" not in table[0]:
            continue
        for row in table:
            stage = row.get("Stage", "")
            if not stage:
                continue
            status = row.get("Status", "")
            target_date = parse_date(row.get("Target Date", ""))
            remind_on = parse_date(row.get("Remind On", ""))
            report, kind = should_report(status, target_date, remind_on, today, horizon)
            if not report:
                continue
            reminders.append(
                Reminder(
                    machine_model=machine_model,
                    work_order=work_order,
                    source=str(path.relative_to(PROJECTS_DIR)).replace("\\", "/"),
                    kind=kind,
                    item=stage,
                    status=status,
                    owner=row.get("Owner", ""),
                    due_date=target_date,
                    remind_on=remind_on,
                    message=row.get("Risk / Blocker", ""),
                )
            )
    return reminders


def scan_issues(path: Path, today: date, horizon: date) -> list[Reminder]:
    reminders: list[Reminder] = []
    machine_model, work_order = project_context(path)
    for table in read_markdown_tables(path):
        if not table or "ID" not in table[0] or "Issue" not in table[0]:
            continue
        for row in table:
            issue_id = row.get("ID", "")
            issue = row.get("Issue", "")
            if not issue_id and not issue:
                continue
            status = row.get("Status", "")
            target_date = parse_date(row.get("Target Date", row.get("Due Date", "")))
            remind_on = parse_date(row.get("Remind On", ""))
            report, kind = should_report(status, target_date, remind_on, today, horizon)
            if not report:
                continue
            reminders.append(
                Reminder(
                    machine_model=machine_model,
                    work_order=work_order,
                    source=str(path.relative_to(PROJECTS_DIR)).replace("\\", "/"),
                    kind=kind,
                    item=f"{issue_id} {issue}".strip(),
                    status=status,
                    owner=row.get("Owner", ""),
                    due_date=target_date,
                    remind_on=remind_on,
                    message=row.get("Next Action", row.get("Impact", "")),
                )
            )
    return reminders


def scan_projects(today: date, days: int) -> list[Reminder]:
    horizon = today + timedelta(days=days)
    reminders: list[Reminder] = []
    if not PROJECTS_DIR.exists():
        return reminders

    for path in sorted(PROJECTS_DIR.rglob("schedule.md")):
        reminders.extend(scan_schedule(path, today, horizon))
    for path in sorted(PROJECTS_DIR.rglob("issues.md")):
        reminders.extend(scan_issues(path, today, horizon))
    return reminders


def format_date(value: date | None) -> str:
    return value.isoformat() if value else ""


def print_report(reminders: list[Reminder], today: date, days: int) -> None:
    print(f"# Project Reminder Report ({today.isoformat()}, next {days} days)")
    print()
    if not reminders:
        print("No due or upcoming reminders found.")
        return

    print("| Kind | Machine Model | Work Order | Source | Item | Status | Owner | Target Date | Remind On | Message |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for reminder in sorted(
        reminders,
        key=lambda item: (
            item.due_date or date.max,
            item.remind_on or date.max,
            item.machine_model,
            item.work_order,
            item.item,
        ),
    ):
        print(
            "| "
            + " | ".join(
                [
                    reminder.kind,
                    reminder.machine_model,
                    reminder.work_order,
                    reminder.source,
                    reminder.item,
                    reminder.status,
                    reminder.owner,
                    format_date(reminder.due_date),
                    format_date(reminder.remind_on),
                    reminder.message,
                ]
            )
            + " |"
        )


def main() -> None:
    args = parse_args()
    today = date.fromisoformat(args.date)
    reminders = scan_projects(today=today, days=args.days)
    print_report(reminders, today=today, days=args.days)


if __name__ == "__main__":
    main()
