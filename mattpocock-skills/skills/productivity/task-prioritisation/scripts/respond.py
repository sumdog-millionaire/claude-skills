"""Show or add to the Response cell of feedback sheet rows, stamping each addition with the writer's initials and the date.

Run from the project root:
    python respond.py docs/agents/task-prioritisation.json "<feedback workbook>" ROW [ROW ...] [--initials JC --text "<note>"]

Without --text it prints each row's feedback and current response and writes nothing.
With --initials and --text it appends "*JC - 13/11* <note>" to each row's response, after any response already there, and reads the cell back.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import openpyxl


def stamp(initials: str, text: str, today: datetime) -> str:
    """The note as the sheet shows it: initials and day/month in italics, then the text."""
    return f"*{initials} - {today.strftime('%d/%m')}* {text.strip()}"


def main(config_path: Path, workbook_path: Path, row_numbers: list[int], initials: str | None, text: str | None) -> None:
    """Print each row's response, then append the stamped note to each when there is one."""
    sheet_config = json.loads(config_path.read_text(encoding="utf-8"))["sheet"]
    columns = sheet_config["columns"]
    writing = text is not None
    if writing:
        # Opening for writing fails while someone holds the workbook open, so nothing is half written.
        with open(workbook_path, "r+b"):
            pass
    workbook = openpyxl.load_workbook(workbook_path)
    sheet = workbook[sheet_config["tab"]]
    for number in row_numbers:
        feedback = sheet.cell(number, columns["feedback"]).value
        if feedback is None:
            raise ValueError(f"Row {number} has no feedback, so it is not a feedback row")
        existing = sheet.cell(number, columns["response"]).value
        print(f"row {number}: {str(feedback)[:80]}\n  response: {existing}")
        if writing:
            note = stamp(initials, text, datetime.now())
            sheet.cell(number, columns["response"]).value = f"{existing}\n\n{note}" if existing else note
    if not writing:
        return
    workbook.save(workbook_path)
    check = openpyxl.load_workbook(workbook_path)[sheet_config["tab"]]
    for number in row_numbers:
        print(f"row {number} column {columns['response']}: {check.cell(number, columns['response']).value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("config", type=Path)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("rows", type=int, nargs="+")
    parser.add_argument("--initials")
    parser.add_argument("--text")
    arguments = parser.parse_args()
    if (arguments.initials is None) != (arguments.text is None):
        parser.error("--initials and --text go together")
    main(arguments.config, arguments.workbook, arguments.rows, arguments.initials, arguments.text)
