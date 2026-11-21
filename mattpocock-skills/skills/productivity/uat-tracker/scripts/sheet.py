"""Read and write a UAT feedback sheet described by a project's uat-tracker.json, through the Excel running on this machine.

Run from the project root, on Windows with Excel desktop open:
  new   <config> <workbook>   build an empty feedback sheet from the config, refusing if the file exists
  rows  <config> <workbook> [--open]   print every row with feedback as one JSON line; --open leaves out closed rows
  ids   <config> <workbook> [--dry-run]   give each row with feedback and no UID the prefix and the next number
  add   <config> <workbook> --tester NAME --type TYPE --status S --priority P --owner CODE[,CODE] [--legacy ANSWER] --feedback TEXT [--feedback TEXT ...]
        [--reference REF] [--links TEXT] [--response TEXT --by INITIALS] [--issue URL] [--dry-run]   add complete rows after the last one, dated today, and give them UIDs
  write <config> <workbook> --id UID [--id UID ...] [--tester NAME] [--status S] [--priority P] [--owner CODE[,CODE]] [--legacy ANSWER] [--response TEXT --by INITIALS] [--issue URL] [--dry-run]
  release <config> <workbook> --released DATETIME --notes FILE [--dry-run]   add one row per change in FILE to the release notes tab, adding the tab when it is missing
--legacy is required on add when the config names a legacy column, and refused when it does not.
Every change goes cell by cell through Excel, so it merges with people editing the sheet at the same time.
A change prints every cell it sets, backs the workbook up, saves, and reads each cell back; --dry-run only prints.
new writes a file nobody has open yet, so it builds it directly with openpyxl.
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

import openpyxl
import pywintypes
import win32com.client
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo
from win32com.client import CDispatch

# The new sheet's rows run from the header to here; Excel extends the table's dropdowns as rows are added
LAST_ROW = 300

# One cell to set: sheet row number, column number, value
Change = tuple[int, int, object]

# The Type and legacy dropdowns' choices, shared by new's dropdowns and the add and write flags
TYPES = ["Bug", "Feature request", "Question"]
LEGACY_ANSWERS = ["Yes", "No", "Not applicable"]


def open_in_excel(path: Path) -> tuple[CDispatch, bool]:
    """Return the workbook from the running Excel and whether this call opened it; refuse a different file of the same name."""
    try:
        excel = win32com.client.GetActiveObject("Excel.Application")
    except pywintypes.com_error:
        raise SystemExit("Excel is not running on this machine; open Excel first. Nothing read or saved.")
    for book in excel.Workbooks:
        if book.Name == path.name:
            # A cloud workbook shows its web address; a local one must be this very file, not a downloaded copy
            if not book.FullName.startswith("https://") and Path(book.FullName).resolve() != path.resolve():
                raise SystemExit(f"A different {path.name} is open in Excel ({book.FullName}); close it first. Nothing read or saved.")
            return book, False
    return excel.Workbooks.Open(str(path.resolve())), True


def plain(value: object) -> object:
    """Return a cell value from Excel with whole numbers as int and dates without Excel's time zone."""
    # Excel hands every number over as a float, so a priority of 1 arrives as 1.0
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    return value


def read_table(sheet: CDispatch) -> dict[int, dict[int, object]]:
    """Read the tab's used range in one call: each sheet row number maps each column number to its value."""
    used = sheet.UsedRange
    return {
        number: {column: plain(value) for column, value in enumerate(values, start=used.Column)}
        for number, values in enumerate(used.Value, start=used.Row)
    }


def header(table: dict[int, dict[int, object]], columns: dict[str, str]) -> tuple[int, dict[str, int]]:
    """Return the header row's number and each column key's column number; the header row is the first holding every configured header."""
    wanted = set(columns.values())
    for number, row in table.items():
        found = {value: column for column, value in row.items() if isinstance(value, str) and value in wanted}
        if len(found) == len(wanted):
            return number, {key: found[text] for key, text in columns.items()}
    raise SystemExit(f"No row holds every configured header: {sorted(wanted)}")


def read_rows(table: dict[int, dict[int, object]], config: dict) -> tuple[dict[str, int], list[dict]]:
    """Return the column map and every row below the header that has feedback, each with its sheet row number."""
    header_row, columns = header(table, config["sheet"]["columns"])
    rows = []
    for number, row in table.items():
        values = {key: row[column] for key, column in columns.items()}
        # A row without feedback is an empty or formatting-only row
        if number <= header_row or values["feedback"] in (None, ""):
            continue
        rows.append({"row": number, **values})
    return columns, rows


def uid_number(uid: object, prefix: str) -> int:
    """Return the number after the configured prefix in a UID cell, such as 12 from "ID_12"."""
    text = str(uid)
    if not text.startswith(prefix):
        raise SystemExit(f"UID {text!r} does not start with {prefix!r}; fix it in the sheet first. Nothing saved.")
    return int(text[len(prefix):])


def assign_ids(rows: list[dict], columns: dict[str, int], prefix: str) -> tuple[list[Change], list[str]]:
    """Give each row with no UID the prefix and the next number after the largest in the column; refuse duplicates."""
    existing = [uid_number(row["id"], prefix) for row in rows if row["id"] not in (None, "")]
    duplicates = sorted({f"{prefix}{number}" for number in existing if existing.count(number) > 1})
    if duplicates:
        raise SystemExit(f"Duplicate UIDs {duplicates}; fix them in the sheet first. Nothing saved.")
    next_number = max(existing, default=0) + 1
    changes, messages = [], []
    for row in rows:
        if row["id"] in (None, ""):
            uid = f"{prefix}{next_number}"
            changes.append((row["row"], columns["id"], uid))
            messages.append(f"sheet row {row['row']}: {uid}")
            next_number += 1
    return changes, messages


def find_row(rows: list[dict], uid: str) -> dict:
    """Return the one row whose UID cell reads exactly this text."""
    matches = [row for row in rows if str(row["id"]) == uid]
    if len(matches) != 1:
        raise SystemExit(f"UID {uid} matches {len(matches)} rows, not one. Nothing saved.")
    return matches[0]


def owner_codes(text: str, config: dict) -> str:
    """One owner code or several comma-separated, checked against the config and returned in one cell's form, such as "AS, BS"."""
    # Joint owners share one cell, comma-separated and in alphabetical order
    codes = sorted({code.strip() for code in text.split(",")})
    unknown = [code for code in codes if code not in config["owners"]]
    if unknown:
        raise SystemExit(f"Owner {', '.join(map(repr, unknown))} is not one of {list(config['owners'])}. Nothing saved.")
    return ", ".join(codes)


def row_values(config: dict, args: argparse.Namespace) -> dict[str, object]:
    """Check the tester, status, priority, owner and legacy answer given on the command line against the config.

    Returns each given value keyed by its column key, ready to write; responses and issues are written per row by the caller.
    """
    values: dict[str, object] = {}
    if args.tester:
        values["tester"] = args.tester
    if args.status:
        if args.status not in config["statuses"].values():
            raise SystemExit(f"Status {args.status!r} is not one of {list(config['statuses'].values())}.")
        values["status"] = args.status
    if args.priority:
        if args.priority not in config["priorities"]:
            raise SystemExit(f"Priority {args.priority!r} is not one of {list(config['priorities'])}.")
        # A priority column usually takes whole numbers, so a digits-only level is written as a number
        values["priority"] = int(args.priority) if args.priority.isdigit() else args.priority
    if args.owner:
        values["owner"] = owner_codes(args.owner, config)
    if args.legacy:
        if "legacy" not in config["sheet"]["columns"]:
            raise SystemExit("The config names no legacy column, so --legacy has nowhere to go. Nothing saved.")
        values["legacy"] = args.legacy
    if args.response and not args.by:
        raise SystemExit("A response needs --by with the writer's initials.")
    return values


def response_line(args: argparse.Namespace) -> str:
    """Return the response as one dated, signed line, such as "- 16 Nov, AB - text"."""
    today = date.today()
    return f"- {today.day} {today:%b}, {args.by} - {args.response}"


def write_rows(table: dict[int, dict[int, object]], config: dict, args: argparse.Namespace) -> tuple[list[Change], list[str]]:
    """Set the given values, add a dated response line on top, and link an issue, on each row named by ID."""
    if not (args.tester or args.status or args.priority or args.owner or args.legacy or args.response or args.issue):
        raise SystemExit("Give --tester, --status, --priority, --owner, --legacy, --response or --issue.")
    values = row_values(config, args)
    columns, rows = read_rows(table, config)
    changes, messages = [], []
    for uid in args.id:
        row = find_row(rows, uid)
        number = row["row"]
        changes += [(number, columns[key], value) for key, value in values.items()]
        if args.response:
            line = response_line(args)
            # Earlier entries stay below the new line, read from the sheet as it is now
            earlier = str(row["response"]).strip() if row["response"] is not None else ""
            changes.append((number, columns["response"], f"{line}\n{earlier}" if earlier else line))
        if args.issue:
            if row["issue"] not in (None, "", args.issue):
                raise SystemExit(f"{uid} already links {row['issue']!r}. Nothing saved.")
            changes.append((number, columns["issue"], args.issue))
        messages.append(f"{uid} (sheet row {number})")
    return changes, messages


def add_rows(table: dict[int, dict[int, object]], config: dict, args: argparse.Namespace) -> tuple[list[Change], list[str]]:
    """Write one complete row per feedback text after the last row with feedback, dated today, then give them UIDs.

    Every row gets the tester, type, status, priority and owner, and the legacy answer when the sheet has that column;
    the reference, links, response and issue are written only when given.
    """
    if "legacy" in config["sheet"]["columns"] and not args.legacy:
        raise SystemExit("This sheet has a legacy column, so give --legacy. Nothing saved.")
    values = row_values(config, args)
    values["type"] = args.type
    if args.reference:
        # Excel reads a digits-only reference as a number, so it is written as one and reads back the same
        values["reference"] = int(args.reference) if args.reference.isdigit() else args.reference
    if args.links:
        values["links"] = args.links
    if args.response:
        values["response"] = response_line(args)
    if args.issue:
        values["issue"] = args.issue
    header_row, columns = header(table, config["sheet"]["columns"])
    _columns, rows = read_rows(table, config)
    number = max((row["row"] for row in rows), default=header_row) + 1
    # Excel takes a date as a datetime at midnight
    values["date"] = datetime.combine(date.today(), datetime.min.time())
    changes, added = [], []
    for text in args.feedback:
        changes.append((number, columns["feedback"], text))
        changes += [(number, columns[key], value) for key, value in values.items()]
        added.append({"row": number, "id": None})
        number += 1
    id_changes, messages = assign_ids(rows + added, columns, config["id_prefix"])
    return changes + id_changes, messages


def release_changes(
    feedback: dict[int, dict[int, object]], release: dict[int, dict[int, object]], config: dict, args: argparse.Namespace
) -> list[Change]:
    """Write one row per change in the notes file after the release tab's last change, each stamped with the release's date and time.

    The notes file is a JSON list of {"change": text, "uids": [UID, ...], "by": owner code or several comma-separated}; every
    owner code must be in the config and every UID on the feedback tab, or nothing is written.
    """
    notes = json.loads(args.notes.read_text(encoding="utf-8"))
    _columns, rows = read_rows(feedback, config)
    known = {str(row["id"]) for row in rows}
    for note in notes:
        note["by"] = owner_codes(note["by"], config)
        unknown = [uid for uid in note["uids"] if uid not in known]
        if unknown:
            raise SystemExit(f"{unknown} is not a UID on the feedback tab. Nothing saved.")
    header_row, columns = header(release, config["release_notes"]["columns"])
    filled = [number for number, row in release.items() if number > header_row and row.get(columns["change"]) not in (None, "")]
    number = max(filled, default=header_row) + 1
    changes = []
    for note in notes:
        values = {"released": args.released, "change": note["change"], "uids": ", ".join(note["uids"]), "by": note["by"]}
        # A change with no UID leaves its cell empty, since Excel reads an empty string back as nothing
        changes += [(number, columns[key], value) for key, value in values.items() if value != ""]
        number += 1
    return changes


def add_release_tab(book: CDispatch, config: dict) -> CDispatch:
    """Add the release notes tab after the last tab, with its headers in bold in the first row, and return it."""
    sheet = book.Worksheets.Add(After=book.Worksheets(book.Worksheets.Count))
    sheet.Name = config["release_notes"]["tab"]
    for number, text in enumerate(config["release_notes"]["columns"].values(), start=1):
        sheet.Cells(1, number).Value = text
        sheet.Cells(1, number).Font.Bold = True
    return sheet


def apply(book: CDispatch, sheet: CDispatch, changes: list[Change], output_dir: Path) -> None:
    """Back the workbook up, set each cell through Excel, save so co-authors get the change at once, then read each cell back."""
    # A cloud workbook merges with co-authors only while AutoSave is on; a local file has no co-authors
    if book.FullName.startswith("https://") and not book.AutoSaveOn:
        raise SystemExit("AutoSave is off for this cloud workbook, so the change would not merge with co-authors; turn it on in Excel. Nothing saved.")
    output_dir.mkdir(parents=True, exist_ok=True)
    backup = output_dir / f"backup-{datetime.now():%Y%m%d-%H%M%S}-{book.Name}"
    book.SaveCopyAs(str(backup.resolve()))
    print(f"workbook: {book.FullName}\nbackup: {backup}")
    for number, column, value in changes:
        sheet.Cells(number, column).Value = value
    book.Save()
    wrong = [f"{get_column_letter(column)}{number}" for number, column, value in changes if plain(sheet.Cells(number, column).Value) != value]
    if wrong:
        raise SystemExit(f"Excel holds a different value from the one written in {wrong}; check them in the sheet.")


def new_workbook(config: dict, path: Path) -> None:
    """Build an empty feedback sheet from the config: UID first and locked, dropdowns from the config, a guide tab and a names tab; a configured legacy column compares each bug with the system being replaced."""
    if path.exists():
        raise SystemExit(f"{path} already exists. Nothing saved.")
    columns = config["sheet"]["columns"]
    statuses = config["statuses"]
    legacy = "legacy" in columns
    headers = [
        columns["id"], columns["date"], columns["tester"], columns["type"], columns["reference"], columns["feedback"],
        *([columns["legacy"]] if legacy else []), columns["links"],
        columns["status"], columns["response"], columns["priority"], columns["owner"], columns["issue"],
    ]
    # Each header's column letter, such as {"Status": "H"}
    letter = {text: get_column_letter(number) for number, text in enumerate(headers, start=1)}

    book = openpyxl.Workbook()
    sheet = book.active
    sheet.title = config["sheet"]["tab"]
    sheet["A1"] = f"{config['tracker']['project']} | UAT feedback"
    sheet["A1"].font = Font(size=14, bold=True)
    for number, text in enumerate(headers, start=1):
        sheet.cell(3, number, text)
        wide = text in (columns["feedback"], columns["response"])
        sheet.column_dimensions[get_column_letter(number)].width = 60 if wide else 16
    style = TableStyleInfo(name="TableStyleLight1", showRowStripes=True)
    sheet.add_table(Table(displayName="FeedbackLog", ref=f"A3:{letter[headers[-1]]}{LAST_ROW}", tableStyleInfo=style))
    sheet.freeze_panes = "B4"

    # The UID column is grey so it reads as a label, and long text wraps
    for number in range(4, LAST_ROW + 1):
        sheet[f"{letter[columns['id']]}{number}"].fill = PatternFill("solid", fgColor="E7E6E6")
        for text in (columns["feedback"], columns["response"]):
            sheet[f"{letter[text]}{number}"].alignment = Alignment(wrap_text=True, vertical="top")

    # A custom rule of FALSE makes Excel refuse anything typed; validation does not apply to the script's writes
    lock = DataValidation(
        type="custom", formula1="FALSE", showInputMessage=True, promptTitle=columns["id"],
        prompt="Filled in automatically. Quote it when you refer to a row.",
        errorStyle="stop", errorTitle=columns["id"], error="This is filled in automatically. Leave it blank.",
    )
    rules = {
        columns["id"]: lock,
        columns["tester"]: DataValidation(type="list", formula1="Testers"),
        columns["type"]: DataValidation(type="list", formula1=f'"{",".join(TYPES)}"'),
        columns["status"]: DataValidation(type="list", formula1=f'"{",".join(statuses.values())}"'),
        columns["priority"]: DataValidation(type="list", formula1=f'"{",".join(config["priorities"])}"'),
        # A warning, not a stop, so joint owners such as "AS, BS" can be typed beside the single codes listed
        columns["owner"]: DataValidation(type="list", formula1=f'"{",".join(config["owners"])}"', errorStyle="warning"),
    }
    if legacy:
        rules[columns["legacy"]] = DataValidation(type="list", formula1=f'"{",".join(LEGACY_ANSWERS)}"')
    for text, rule in rules.items():
        rule.showErrorMessage = True
        sheet.add_data_validation(rule)
        rule.add(f"{letter[text]}4:{letter[text]}{LAST_ROW}")
    status_range = f"{letter[columns['status']]}4:{letter[columns['status']]}{LAST_ROW}"
    for key, colour in (("open", "FFC7CE"), ("in_progress", "FFEB9C"), ("built", "BDD7EE"), ("closed", "C6EFCE")):
        rule = CellIsRule(operator="equal", formula=[f'"{statuses[key]}"'], fill=PatternFill(bgColor=colour))
        sheet.conditional_formatting.add(status_range, rule)

    guide = book.create_sheet("How to use")
    guide["A1"] = "How to use"
    guide["A1"].font = Font(size=14, bold=True)
    lines = [
        ("Where to write", f"Use the next empty row in {sheet.title}. Add one bug, request or question per row."),
        (columns["id"], "Filled in automatically. Quote it when you refer to a row; Excel refuses anything typed there."),
        (f"{columns['date']}, {columns['tester']}, {columns['type']}", "Enter the date and choose your name and the type from the dropdowns."),
        (columns["reference"], "The record the feedback is about, such as an order or booking number, when there is one."),
        (columns["feedback"], "For a bug, say what you did, what happened and what you expected. For a request, say what you would change."),
        (columns["links"], "A sharing link to screenshots or further information. Make sure the reviewing team can open it."),
        (columns["status"], f"{statuses['open']} (red): not yet being worked on. {statuses['in_progress']} (amber): work is under way. {statuses['built']} (blue): the fix is built and waits to go live where you test. {statuses['closed']} (green): live where you test, or no further action, and the response says why."),
        ("Reviewing team", f"{columns['status']}, {columns['response']}, {columns['priority']}, {columns['owner']} and {columns['issue']} are filled in by the reviewing team. Testers can leave them blank."),
        (columns["priority"], " ".join(f"{level}: {meaning}." for level, meaning in config["priorities"].items()) + " A request or question takes the priority of the problem it solves."),
        ("Names", "Add testers on the Names tab, directly below the list without gaps."),
    ]
    if legacy:
        lines.insert(5, (columns["legacy"], "For a bug, try the same thing in the old system and choose Yes or No. Choose Not applicable if it has no equivalent, or for a request or question."))
    for number, (label, text) in enumerate(lines, start=3):
        guide.cell(number, 1, label).font = Font(bold=True)
        guide.cell(number, 2, text).alignment = Alignment(wrap_text=True, vertical="top")
    guide.column_dimensions["A"].width = 22
    guide.column_dimensions["B"].width = 100

    names = book.create_sheet("Names")
    names["A1"] = "Tester names"
    names["A2"] = "Add each tester below, without blank rows; the Tester dropdown reads this list."
    names["A3"], names["C3"], names["D3"] = "Tester", "Owner code", "Owner"
    for number, (code, owner) in enumerate(config["owners"].items(), start=4):
        names.cell(number, 3, code)
        names.cell(number, 4, owner["name"])
    # The dropdown grows with the list: from A4 down as many cells as hold a name, never fewer than one
    book.defined_names["Testers"] = DefinedName("Testers", attr_text="OFFSET(Names!$A$4,0,0,MAX(1,COUNTA(Names!$A$4:$A$1000)),1)")

    releases = book.create_sheet(config["release_notes"]["tab"])
    for number, text in enumerate(config["release_notes"]["columns"].values(), start=1):
        releases.cell(1, number, text).font = Font(bold=True)
        releases.column_dimensions[get_column_letter(number)].width = 60 if text == config["release_notes"]["columns"]["change"] else 18
    book.save(path)
    print(f"workbook: {path}")


def main() -> None:
    """Parse the command line and run one command."""
    # Windows writes to the console in its own code page, so rows printed with a curly quote would not read back as UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
    parser =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("new", "rows", "ids", "add", "write", "release"):
        command = commands.add_parser(name)
        command.add_argument("config", type=Path)
        command.add_argument("workbook", type=Path)
        if name == "new":
            continue
        if name == "rows":
            command.add_argument("--open", action="store_true", help="leave out rows whose status is the closed word")
        else:
            command.add_argument("--dry-run", action="store_true", help="print the cells this would set and set none")
    for name in ("add", "write"):
        command = commands.choices[name]
        # A new row must be complete; write changes only what it is given
        required = name == "add"
        command.add_argument("--tester", required=required, help="who raised the row, as the tester dropdown names them; whoever originated it")
        command.add_argument("--status", required=required, help="one of the config's status words")
        command.add_argument("--priority", required=required, help="one of the config's priorities, as agreed with the user")
        command.add_argument("--owner", required=required, help="one of the config's owner codes, or several comma-separated, written in alphabetical order")
        command.add_argument("--legacy", choices=LEGACY_ANSWERS, help="the legacy column's answer; required on add when the config names that column")
        command.add_argument("--response")
        command.add_argument("--by", help="the writer's initials, signed on the response")
        command.add_argument("--issue", help="the tracker issue's address")
    add = commands.choices["add"]
    add.add_argument("--type", required=True, choices=TYPES, help="the type column's value for every row added")
    add.add_argument("--feedback", action="append", required=True, help="one row's feedback; repeat for several rows")
    add.add_argument("--reference", help="the record the feedback is about, such as a booking or order number")
    add.add_argument("--links", help="links to screenshots or further information")
    write = commands.choices["write"]
    write.add_argument("--id", action="append", required=True, help="a row's UID as the sheet shows it; repeat for several rows")
    release = commands.choices["release"]
    release.add_argument("--released", required=True, type=datetime.fromisoformat, help="when the release went live, such as 2026-03-16T18:30")
    release.add_argument("--notes", required=True, type=Path, help='a JSON list of {"change": text, "uids": [UID, ...], "by": owner code, or several comma-separated}')
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.command == "new":
        new_workbook(config, args.workbook)
        return
    book, opened = open_in_excel(args.workbook)
    try:
        sheet = book.Worksheets(config["sheet"]["tab"])
        table = read_table(sheet)
        if args.command == "rows":
            _columns, rows = read_rows(table, config)
            for row in rows:
                # A blank status counts as open, so only the closed word is left out
                if args.open and row["status"] == config["statuses"]["closed"]:
                    continue
                print(json.dumps(row, default=str, ensure_ascii=False))
            return
        if args.command == "ids":
            columns, rows = read_rows(table, config)
            changes, messages = assign_ids(rows, columns, config["id_prefix"])
        elif args.command == "add":
            changes, messages = add_rows(table, config, args)
        elif args.command == "write":
            changes, messages = write_rows(table, config, args)
        else:
            notes_tab = config["release_notes"]
            tab_exists = notes_tab["tab"] in [tab.Name for tab in book.Worksheets]
            # A missing tab reads as its header row alone, which this run adds once every check has passed
            feedback = table
            table = read_table(book.Worksheets(notes_tab["tab"])) if tab_exists else {1: dict(enumerate(notes_tab["columns"].values(), start=1))}
            changes = release_changes(feedback, table, config, args)
            messages = [] if tab_exists else [f"Adds the {notes_tab['tab']} tab with its headers"]
        for line in messages:
            print(line)
        for number, column, value in changes:
            # A cell beyond the used range is empty, so it is missing from the table
            before = table.get(number, {}).get(column)
            print(f"{get_column_letter(column)}{number}: {before!r} -> {value!r}")
        if args.dry_run or not changes:
            return
        if args.command == "release":
            sheet = book.Worksheets(notes_tab["tab"]) if tab_exists else add_release_tab(book, config)
        apply(book, sheet, changes, Path(config["output_dir"]))
    finally:
        # A workbook this run opened is closed again; one the user had open stays open
        if opened:
            book.Close(SaveChanges=False)


if __name__ == "__main__":
    main()
