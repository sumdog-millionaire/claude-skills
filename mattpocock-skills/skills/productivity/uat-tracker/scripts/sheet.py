"""Read and write a UAT feedback sheet described by a project's uat-tracker.json, through the Excel running on this machine.

Run from the project root, on Windows with Excel desktop open:
  new   <config> <workbook> [--legacy] build an empty feedback sheet from the config, refusing if the file exists
  rows  <config> <workbook> [--open]   print every row with feedback as one JSON line; --open leaves out closed rows
  ids   <config> <workbook> [--dry-run]   give each row with feedback and no UID the prefix and the next number
  add   <config> <workbook> --type TYPE --feedback TEXT [--feedback TEXT ...] [--dry-run]   add rows after the last one, dated today, and give them UIDs
  write <config> <workbook> --id UID [--id UID ...] [--status S] [--priority P] [--owner CODE[,CODE]] [--response TEXT --by INITIALS] [--issue URL] [--dry-run]
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


def write_rows(table: dict[int, dict[int, object]], config: dict, args: argparse.Namespace) -> tuple[list[Change], list[str]]:
    """Set status, priority and owner, add a dated response line on top, and link an issue, on each row named by ID."""
    if not (args.status or args.priority or args.owner or args.response or args.issue):
        raise SystemExit("Give --status, --priority, --owner, --response or --issue.")
    if args.status and args.status not in config["statuses"].values():
        raise SystemExit(f"Status {args.status!r} is not one of {list(config['statuses'].values())}.")
    if args.priority and args.priority not in config["priorities"]:
        raise SystemExit(f"Priority {args.priority!r} is not one of {list(config['priorities'])}.")
    owner = None
    if args.owner:
        # Joint owners share one cell, comma-separated and in alphabetical order, such as "AS, BS"
        codes = sorted({code.strip() for code in args.owner.split(",")})
        unknown = [code for code in codes if code not in config["owners"]]
        if unknown:
            raise SystemExit(f"Owner {unknown} is not one of {list(config['owners'])}.")
        owner = ", ".join(codes)
    if args.response and not args.by:
        raise SystemExit("A response needs --by with the writer's initials.")
    columns, rows = read_rows(table, config)
    today = date.today()
    changes, messages = [], []
    for uid in args.id:
        row = find_row(rows, uid)
        number = row["row"]
        if args.status:
            changes.append((number, columns["status"], args.status))
        if args.priority:
            # A priority column usually takes whole numbers, so a digits-only level is written as a number
            changes.append((number, columns["priority"], int(args.priority) if args.priority.isdigit() else args.priority))
        if owner:
            changes.append((number, columns["owner"], owner))
        if args.response:
            line = f"- {today.day} {today:%b}, {args.by} - {args.response}"
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
    """Write each feedback text with today's date and the type into the rows after the last row with feedback, then give them UIDs."""
    # Type is found by the header new gives it, so a sheet without it stops here
    header_row, columns = header(table, {**config["sheet"]["columns"], "type": "Type"})
    _columns, rows = read_rows(table, config)
    number = max((row["row"] for row in rows), default=header_row) + 1
    # Excel takes a date as a datetime at midnight
    today = datetime.combine(date.today(), datetime.min.time())
    changes, added = [], []
    for text in args.feedback:
        changes += [(number, columns["feedback"], text), (number, columns["date"], today), (number, columns["type"], args.type)]
        added.append({"row": number, "id": None})
        number += 1
    id_changes, messages = assign_ids(rows + added, columns, config["id_prefix"])
    return changes + id_changes, messages


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


def new_workbook(config: dict, path: Path, legacy: bool) -> None:
    """Build an empty feedback sheet from the config: UID first and locked, dropdowns from the config, a guide tab and a names tab; legacy adds a column comparing with the system being replaced."""
    if path.exists():
        raise SystemExit(f"{path} already exists. Nothing saved.")
    columns = config["sheet"]["columns"]
    statuses = config["statuses"]
    legacy_header = "Same issue in legacy?"
    headers = [
        columns["id"], columns["date"], columns["tester"], "Type", "Reference", columns["feedback"], *([legacy_header] if legacy else []), "Links",
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
        "Type": DataValidation(type="list", formula1='"Bug,Feature request,Question"'),
        columns["status"]: DataValidation(type="list", formula1=f'"{",".join(statuses.values())}"'),
        columns["priority"]: DataValidation(type="list", formula1=f'"{",".join(config["priorities"])}"'),
        # A warning, not a stop, so joint owners such as "AS, BS" can be typed beside the single codes listed
        columns["owner"]: DataValidation(type="list", formula1=f'"{",".join(config["owners"])}"', errorStyle="warning"),
    }
    if legacy:
        rules[legacy_header] = DataValidation(type="list", formula1='"Yes,No,Not applicable"')
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
        (f"{columns['date']}, {columns['tester']}, Type", "Enter the date and choose your name and the type from the dropdowns."),
        ("Reference", "The record the feedback is about, such as an order or booking number, when there is one."),
        (columns["feedback"], "For a bug, say what you did, what happened and what you expected. For a request, say what you would change."),
        ("Links", "A sharing link to screenshots or further information. Make sure the reviewing team can open it."),
        (columns["status"], f"{statuses['open']} (red): not yet being worked on. {statuses['in_progress']} (amber): work is under way. {statuses['built']} (blue): the fix is built and waits to go live where you test. {statuses['closed']} (green): live where you test, or no further action, and the response says why."),
        ("Reviewing team", f"{columns['status']}, {columns['response']}, {columns['priority']}, {columns['owner']} and {columns['issue']} are filled in by the reviewing team. Testers can leave them blank."),
        (columns["priority"], " ".join(f"{level}: {meaning}." for level, meaning in config["priorities"].items()) + " A request or question takes the priority of the problem it solves."),
        ("Names", "Add testers on the Names tab, directly below the list without gaps."),
    ]
    if legacy:
        lines.insert(5, (legacy_header, "For a bug, try the same thing in the old system and choose Yes or No. Choose Not applicable if it has no equivalent, or for a request or question."))
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
    book.save(path)
    print(f"workbook: {path}")


def main() -> None:
    """Parse the command line and run one command."""
    # Windows writes to the console in its own code page, so rows printed with a curly quote would not read back as UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
    parser =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("new", "rows", "ids", "add", "write"):
        command = commands.add_parser(name)
        command.add_argument("config", type=Path)
        command.add_argument("workbook", type=Path)
        if name == "new":
            command.add_argument("--legacy", action="store_true", help="add a column comparing each bug with the system being replaced")
            continue
        if name == "rows":
            command.add_argument("--open", action="store_true", help="leave out rows whose status is the closed word")
        else:
            command.add_argument("--dry-run", action="store_true", help="print the cells this would set and set none")
    add = commands.choices["add"]
    add.add_argument("--type", required=True, choices=["Bug", "Feature request", "Question"], help="the Type column's value for every row added")
    add.add_argument("--feedback", action="append", required=True, help="one row's feedback; repeat for several rows")
    write = commands.choices["write"]
    write.add_argument("--id", action="append", required=True, help="a row's UID as the sheet shows it; repeat for several rows")
    write.add_argument("--status")
    write.add_argument("--priority", help="one of the config's priorities")
    write.add_argument("--owner", help="one of the config's owner codes, or several comma-separated, written in alphabetical order")
    write.add_argument("--response")
    write.add_argument("--by", help="the writer's initials, signed on the response")
    write.add_argument("--issue", help="the tracker issue's address")
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.command == "new":
        new_workbook(config, args.workbook, args.legacy)
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
        else:
            changes, messages = write_rows(table, config, args)
        for line in messages:
            print(line)
        for number, column, value in changes:
            # A cell beyond the used range is empty, so it is missing from the table
            before = table.get(number, {}).get(column)
            print(f"{get_column_letter(column)}{number}: {before!r} -> {value!r}")
        if args.dry_run or not changes:
            return
        apply(book, sheet, changes, Path(config["output_dir"]))
    finally:
        # A workbook this run opened is closed again; one the user had open stays open
        if opened:
            book.Close(SaveChanges=False)


if __name__ == "__main__":
    main()
