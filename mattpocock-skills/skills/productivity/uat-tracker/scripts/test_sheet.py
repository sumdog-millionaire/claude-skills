"""Check sheet.py's guards on a small workbook built in a temporary folder. Run with Excel open: python test_sheet.py"""

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

import openpyxl
import win32com.client
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

SCRIPT = Path(__file__).with_name("sheet.py")
RELEASE_NOTES = {
    "tab": "Change log",
    "columns": {"released": "Released", "level": "Major or minor", "change": "Change", "requester": "Requested by", "uids": "Feedback UID"},
}
CONFIG = {
    "workbook": "test",
    "output_dir": "out",
    "id_prefix": "ID_",
    "sheet": {
        "tab": "Feedback Log",
        "columns": {
            "id": "ID", "feedback": "Feedback", "status": "Status", "response": "Response",
            "priority": "Priority", "owner": "Assigned to", "issue": "Tracker issue", "tester": "Tester",
        },
    },
    "release_notes": RELEASE_NOTES,
    "statuses": {"open": "Open", "in_progress": "In progress", "closed": "Closed"},
    "priorities": {"1": "Wrong or broken", "2": "Seriously harms the experience", "3": "A minor imperfection"},
    "owners": {"B": {"name": "Sam Example", "initials": "SE", "layer": "back end"}, "F": {"name": "Fay Example", "initials": "FE", "layer": "front end"}},
    "tracker": {"project": "Example", "queue_label": "uat-queue"},
}
# new builds every column the script knows, so its config names them all
FULL_CONFIG = {
    **CONFIG,
    "sheet": {
        "tab": "Feedback Log",
        "columns": {
            "id": "UID", "date": "Date", "tester": "Tester", "type": "Type", "reference": "Booking ID", "feedback": "Feedback",
            "links": "Links", "status": "Status", "response": "Response", "priority": "Priority", "owner": "Assigned to", "issue": "Tracker issue",
        },
    },
    "statuses": {"open": "Open", "in_progress": "In progress", "built": "Built", "closed": "Closed"},
}


def build(folder: Path) -> Path:
    """Write a workbook with a title row, a header row, a dropdown, a conditional format and four rows (one blank)."""
    book = openpyxl.Workbook()
    sheet = book.active
    sheet.title = "Feedback Log"
    book.create_sheet("Names")
    sheet.append(["UAT feedback"])
    sheet.append(["Feedback", "ID", "Status", "Response", "Priority", "Assigned to", "Tracker issue", "Tester"])
    sheet.append(["Price wrong", "ID_4", "Open", "Earlier note", 1, "B", None, "Eli Example"])
    sheet.append(["Map missing", None, None, None, 2, "B", "https://tracker/ENG-1", "Ella Example"])
    sheet.append([None, None, None, None, None, None, None, None])
    sheet.append(["Logo blurry", None, "Open", None, 3, None, None, "Eli Example"])
    dropdown = DataValidation(type="list", formula1='"Open,In progress,Closed"')
    sheet.add_data_validation(dropdown)
    dropdown.add("C3:C100")
    sheet.conditional_formatting.add("E3:E100", CellIsRule(operator="equal", formula=["1"], fill=PatternFill(bgColor="FFC7CE")))
    path = folder / "feedback.xlsx"
    book.save(path)
    (folder / "config.json").write_text(json.dumps(CONFIG))
    (folder / "full_config.json").write_text(json.dumps(FULL_CONFIG))
    return path


def run(folder: Path, *arguments: str) -> subprocess.CompletedProcess:
    """Run sheet.py from the folder, as an agent would from the project root."""
    return subprocess.run([sys.executable, str(SCRIPT), *arguments], cwd=folder, capture_output=True, text=True)


def cell(path: Path, coordinate: str, tab: str = "Feedback Log") -> object:
    """Read one cell of a tab from the saved file."""
    return openpyxl.load_workbook(path)[tab][coordinate].value


def notes(folder: Path, name: str, changes: list[dict]) -> str:
    """Write a release's changes to a JSON file in the folder and return its name."""
    (folder / name).write_text(json.dumps(changes))
    return name


def main() -> None:
    """Run each guard against a fresh workbook."""
    with tempfile.TemporaryDirectory() as temp:
        folder = Path(temp).resolve()
        workbook = build(folder)
        base = ["config.json", "feedback.xlsx"]

        # A dry run prints the change and sets nothing
        result = run(folder, "ids", *base, "--dry-run")
        assert result.returncode == 0, result.stderr
        assert cell(workbook, "B4") is None and "B4: None -> 'ID_5'" in result.stdout

        # UIDs continue from the largest, with the prefix, skipping the blank row
        result = run(folder, "ids", *base)
        assert result.returncode == 0, result.stderr
        assert (cell(workbook, "B4"), cell(workbook, "B6")) == ("ID_5", "ID_6")

        # A response goes on top, signed and dated, with the earlier note kept below
        result = run(folder, "write", *base, "--id", "ID_4", "--status", "In progress", "--response", "Found the cause", "--by", "SE")
        assert result.returncode == 0, result.stderr
        today = date.today()
        assert cell(workbook, "D3") == f"- {today.day} {today:%b}, SE - Found the cause\nEarlier note"
        assert cell(workbook, "C3") == "In progress"

        # An unknown status is refused and nothing is saved
        result = run(folder, "write", *base, "--id", "ID_4", "--status", "Done")
        assert result.returncode != 0 and cell(workbook, "C3") == "In progress"

        # Priority is written as a number and owner as its code; an unknown priority is refused and nothing is saved
        assert run(folder, "write", *base, "--id", "ID_6", "--priority", "1", "--owner", "B").returncode == 0
        assert (cell(workbook, "E6"), cell(workbook, "F6")) == (1, "B")
        assert run(folder, "write", *base, "--id", "ID_6", "--priority", "4").returncode != 0 and cell(workbook, "E6") == 1

        # A different issue link is refused; the same one is accepted
        assert run(folder, "write", *base, "--id", "ID_5", "--issue", "https://tracker/ENG-2").returncode != 0
        assert run(folder, "write", *base, "--id", "ID_5", "--issue", "https://tracker/ENG-1").returncode == 0

        # Duplicate UIDs, or a UID without the prefix, stop the ID run
        book = openpyxl.load_workbook(workbook)
        book["Feedback Log"]["B6"] = "ID_4"
        book.save(workbook)
        assert "Duplicate UIDs ['ID_4']" in run(folder, "ids", *base).stderr
        book["Feedback Log"]["B6"] = 6
        book.save(workbook)
        assert "does not start with 'ID_'" in run(folder, "ids", *base).stderr
        book["Feedback Log"]["B6"] = "ID_6"
        book.save(workbook)

        # rows --open leaves out the closed row and keeps the in-progress and open rows
        assert run(folder, "write", *base, "--id", "ID_5", "--status", "Closed").returncode == 0
        open_rows = [json.loads(line)["feedback"] for line in run(folder, "rows", *base, "--open", "--owner", "all").stdout.splitlines()]
        assert open_rows == ["Price wrong", "Logo blurry"], open_rows

        # rows --owner keeps every row whose owner cell names the code, alone or beside others; all keeps every row; an unknown code or none is refused
        assert run(folder, "write", *base, "--id", "ID_4", "--owner", "F,B").returncode == 0
        assert run(folder, "write", *base, "--id", "ID_6", "--owner", "F").returncode == 0
        owned = lambda code: [json.loads(line)["feedback"] for line in run(folder, "rows", *base, "--open", "--owner", code).stdout.splitlines()]
        assert owned("B") == ["Price wrong"], owned("B")
        assert owned("F") == ["Price wrong", "Logo blurry"], owned("F")
        assert owned("all") == ["Price wrong", "Logo blurry"], owned("all")
        # none keeps only rows with a blank owner cell
        book = openpyxl.load_workbook(workbook)
        book["Feedback Log"]["F6"] = None
        book.save(workbook)
        assert owned("none") == ["Logo blurry"], owned("none")
        assert "Owner 'Z' is not one of" in run(folder, "rows", *base, "--owner", "Z").stderr
        assert "the following arguments are required: --owner" in run(folder, "rows", *base).stderr

        # A different workbook of the same name open in Excel, such as a downloaded copy, stops every command
        (folder / "other").mkdir()
        other = folder / "other" / "feedback.xlsx"
        shutil.copy2(workbook, other)
        copy_open = win32com.client.GetActiveObject("Excel.Application").Workbooks.Open(str(other))
        result = run(folder, "write", *base, "--id", "ID_6", "--status", "Closed")
        copy_open.Close(SaveChanges=False)
        assert "A different feedback.xlsx is open" in result.stderr, result.stderr
        assert cell(workbook, "C6") == "Open"

        # The dropdown and the conditional format survived every write through Excel
        sheet = openpyxl.load_workbook(workbook)["Feedback Log"]
        assert len(sheet.data_validations.dataValidation) == 1 and len(sheet.conditional_formatting) == 1

        # A release naming a UID the sheet lacks, or a level other than Major or Minor, is refused and writes nothing, not even the tab
        unknown_uid = notes(folder, "unknown_uid.json", [{"change": "Prices add up", "uids": ["ID_99"], "level": "Major"}])
        result = run(folder, "release", *base, "--released", "2026-11-21T18:30", "--notes", unknown_uid)
        assert "ID_99" in result.stderr, result.stderr
        unknown_level = notes(folder, "unknown_level.json", [{"change": "Prices add up", "uids": [], "level": "Huge"}])
        result = run(folder, "release", *base, "--released", "2026-11-21T18:30", "--notes", unknown_level)
        assert "Level 'Huge'" in result.stderr, result.stderr
        assert "Change log" not in openpyxl.load_workbook(workbook).sheetnames

        # A dry run says it would add the tab and adds nothing
        first = notes(folder, "first.json", [
            {"change": "Prices add up", "uids": ["ID_4", "ID_5"], "level": "Major"},
            {"change": "Drafts finish faster", "uids": [], "level": "Minor"},
        ])
        result = run(folder, "release", *base, "--released", "2026-11-21T18:30", "--notes", first, "--dry-run")
        assert result.returncode == 0 and "Adds the Change log tab" in result.stdout, result.stderr
        assert "Change log" not in openpyxl.load_workbook(workbook).sheetnames

        # A release adds the tab and one row per change, each stamped with the release's date and time
        result = run(folder, "release", *base, "--released", "2026-11-21T18:30", "--notes", first)
        assert result.returncode == 0, result.stderr
        released = datetime(2026, 11, 21, 18, 30)
        # The tab is laid out like the feedback tab: a title, a spacer row, headers in row 3, then one row per change
        # Each change names who asked for it, from the Tester cell of each row it answers, once each
        assert cell(workbook, "A1", "Change log") == "Change log"
        rows = [[cell(workbook, f"{column}{row}", "Change log") for column in "ABCDE"] for row in (3, 4, 5)]
        assert rows == [
            ["Released", "Major or minor", "Change", "Requested by", "Feedback UID"],
            [released, "Major", "Prices add up", "Eli Example, Ella Example", "ID_4, ID_5"],
            [released, "Minor", "Drafts finish faster", None, None],
        ], rows

        # The tab is an Excel table that opens filtered to Major, styled like the feedback tab, with a readable date
        log = openpyxl.load_workbook(workbook)["Change log"]
        table = next(iter(log.tables.values()))
        assert table.ref == "A3:E5", table.ref
        assert [(column.colId, column.filters.filter) for column in table.autoFilter.filterColumn] == [(1, ["Major"])]
        assert (log["A3"].font.b, log["A3"].fill.fgColor.rgb, log["A3"].font.color.rgb) == (True, "FFE9EEEB", "FF27342F")
        assert log["C4"].alignment.wrap_text and log["C4"].border.bottom.style == "thin"
        # Excel stores the date format with its spaces and comma escaped by backslashes
        assert log["A4"].number_format.replace("\\", "") == "d mmm yyyy, hh:mm", log["A4"].number_format

        # A later release goes below the last one, and the table grows to hold it
        second = notes(folder, "second.json", [{"change": "Map shows both airports", "uids": ["ID_6"], "level": "Major"}])
        assert run(folder, "release", *base, "--released", "2026-11-28T09:05", "--notes", second).returncode == 0
        assert [cell(workbook, f"{column}6", "Change log") for column in "BCDE"] == ["Major", "Map shows both airports", "Eli Example", "ID_6"]
        assert next(iter(openpyxl.load_workbook(workbook)["Change log"].tables.values())).ref == "A3:E6"

        # new builds a sheet the other commands read, with the UID column locked, leaves the change log tab to release, and never overwrites one
        fresh = folder / "new.xlsx"
        assert run(folder, "new", "full_config.json", "new.xlsx").returncode == 0
        assert "already exists" in run(folder, "new", "full_config.json", "new.xlsx").stderr
        book = openpyxl.load_workbook(fresh)
        lock = next(rule for rule in book["Feedback Log"].data_validations.dataValidation if "A4" in rule.sqref)
        assert (lock.type, lock.formula1) == ("custom", "FALSE")
        assert "Change log" not in book.sheetnames
        dropdowns = len(book["Feedback Log"].data_validations.dataValidation)
        book["Feedback Log"]["F4"] = "Total wrong"
        book.save(fresh)
        assert run(folder, "ids", "full_config.json", "new.xlsx").returncode == 0
        assert cell(fresh, "A4") == "ID_1"

        # add writes the next row dated today, unshifted by any time zone, with its type and the next UID
        result = run(
            folder, "add", "full_config.json", "new.xlsx", "--tester", "Sam Example", "--type", "Bug",
            "--status", "Open", "--priority", "1", "--owner", "B", "--feedback", "Map missing",
        )
        assert result.returncode == 0, result.stderr
        added = [cell(fresh, coordinate) for coordinate in ("A5", "B5", "D5", "F5")]
        assert added == ["ID_2", datetime.combine(date.today(), datetime.min.time()), "Bug", "Map missing"], added

        # new's dropdowns survived the writes through Excel
        assert len(openpyxl.load_workbook(fresh)["Feedback Log"].data_validations.dataValidation) == dropdowns
    print("sheet.py: all checks passed")


if __name__ == "__main__":
    main()
