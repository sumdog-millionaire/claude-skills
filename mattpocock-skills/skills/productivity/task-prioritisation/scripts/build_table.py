"""Build the task prioritisation table: every open tracker issue beside every feedback sheet row, as one local HTML page.

Run from the project root:
    python build_table.py docs/agents/task-prioritisation.json "<feedback workbook>" <output_dir>/issues.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import openpyxl

TEMPLATE = Path(__file__).with_name("template.html")
DATA_MARKER = "/*DATA*/null"


def cell_key(value: object) -> str:
    """A cell's value as it is written in the config's maps: an empty cell is the empty string."""
    return "" if value is None else str(value)


def read_sheet_rows(config: dict, sheet_path: Path) -> list[dict]:
    """Every sheet row with feedback, in the table's words, with the identifier of the issue it links to."""
    sheet_config = config["sheet"]
    columns = sheet_config["columns"]
    prefix = config["issue_url_prefix"]
    sheet = openpyxl.load_workbook(sheet_path, data_only=True)[sheet_config["tab"]]
    rows = []
    for number in range(sheet_config["first_row"], sheet.max_row + 1):
        feedback = sheet.cell(number, columns["feedback"]).value
        if feedback is None:
            continue
        address = sheet.cell(number, columns["issue"]).value
        # The issue cell holds the issue's address; what follows the prefix, up to any slash, is its identifier.
        issue = address.removeprefix(prefix).split("/")[0] if address else None
        rows.append({
            "row": number,
            "feedback": feedback,
            "response": sheet.cell(number, columns["response"]).value,
            "status": sheet_config["status"][cell_key(sheet.cell(number, columns["status"]).value)],
            "priority": sheet_config["priority"][cell_key(sheet.cell(number, columns["priority"]).value)],
            "owner": sheet_config["owner"][cell_key(sheet.cell(number, columns["owner"]).value)],
            "issue": issue,
            "url": prefix + issue if issue else None,
        })
    return rows


def read_issues(config: dict, issues_path: Path) -> list[dict]:
    """The issues saved from the tracker, in the table's words, each with its address."""
    issues = []
    for issue in json.loads(issues_path.read_text(encoding="utf-8")):
        issues.append({
            "id": issue["id"],
            "title": issue["title"],
            "status": config["issue_status"][issue["status"]],
            "priority": config["issue_priority"][issue["priority"]],
            # First names keep the owner column narrow.
            "owner": issue["assignee"].split()[0] if issue["assignee"] else None,
            "milestone": issue["milestone"],
            "queue": config["queue_label"] in issue["labels"],
            "url": config["issue_url_prefix"] + issue["id"],
        })
    return issues


def main(config_path: Path, sheet_path: Path, issues_path: Path) -> None:
    """Write the table page from the config, the feedback workbook and the saved issues."""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    template = TEMPLATE.read_text(encoding="utf-8")
    if DATA_MARKER not in template:
        raise ValueError(f"{TEMPLATE} has lost its data marker {DATA_MARKER}")
    issues = read_issues(config, issues_path)
    rows = read_sheet_rows(config, sheet_path)
    data = {
        "refreshed": datetime.now().strftime("%d %b %Y, %H:%M"),
        "queueLabel": config["queue_label"],
        "issues": issues,
        "rows": rows,
    }
    # A "</" inside the data would close the page's script tag early.
    text = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    output = Path(config["output_dir"]) / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template.replace(DATA_MARKER, text), encoding="utf-8")
    print(f"{len(issues)} issues and {len(rows)} sheet rows written to {output}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
