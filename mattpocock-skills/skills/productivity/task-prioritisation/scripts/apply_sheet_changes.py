"""Write the sheet-row edits saved from the task prioritisation table into the feedback workbook.

Run from the project root:
    python apply_sheet_changes.py docs/agents/task-prioritisation.json "<feedback workbook>" "<changes file>"
"""

import json
import sys
from pathlib import Path

import openpyxl

EDITABLE_FIELDS = ("priority", "owner")


def cell_value(key: str) -> object:
    """A config map key as the cell value it stands for: the empty string is an empty cell, digits are a number."""
    if key == "":
        return None
    return int(key) if key.isdigit() else key


def table_word_to_cell(mapping: dict) -> dict:
    """The config's sheet map turned round, from the table's word to the cell value, refusing a word two cells share."""
    turned = {}
    for key, word in mapping.items():
        if word in turned:
            raise ValueError(f"Two sheet values map to {word!r}, so a change to it cannot be written back")
        turned[word] = cell_value(key)
    return turned


def main(config_path: Path, sheet_path: Path, changes_path: Path) -> None:
    """Write each sheet-row change into its cell, then read every changed cell back."""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    sheet_config = config["sheet"]
    changes = [change for change in json.loads(changes_path.read_text(encoding="utf-8"))["changes"] if change["kind"] == "row"]
    if not changes:
        print("No sheet-row changes to write.")
        return
    # Opening for writing fails while someone holds the workbook open, so a save cannot race them.
    with open(sheet_path, "r+b"):
        pass
    words = {field: table_word_to_cell(sheet_config[field]) for field in EDITABLE_FIELDS}
    workbook = openpyxl.load_workbook(sheet_path)
    sheet = workbook[sheet_config["tab"]]
    written = []
    for change in changes:
        column = sheet_config["columns"][change["field"]]
        # The page sends an empty string for "none", which the maps hold as null.
        sheet.cell(change["row"], column).value = words[change["field"]][change["to"] or None]
        written.append((change["row"], column, change["field"], change["to"]))
    workbook.save(sheet_path)
    check = openpyxl.load_workbook(sheet_path, data_only=True)[sheet_config["tab"]]
    for row, column, field, word in written:
        print(f"row {row} {field}: {word!r} -> cell {check.cell(row, column).value!r}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
