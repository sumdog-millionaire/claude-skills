"""Turn the feedback rows marked for building into Linear issues and write each issue's link back into its rows.

Run from the project root, whose .env holds LINEAR_API_KEY:
    python graduate.py docs/agents/task-prioritisation.json "<feedback workbook>" [--dry-run]

--dry-run checks every lookup and prints the issues it would create, creating and writing nothing; it can read a copy of the workbook.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import openpyxl
from dotenv import load_dotenv

# A sibling module: Python puts this script's folder on the import path when it runs the script.
from linear import run_query

LINEAR_PRIORITY = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4}
TITLE_LENGTH = 80
PROJECT_QUERY = "query Project($id: String!) { project(id: $id) { id teams { nodes { id } } } }"
LABEL_QUERY = "query Label($name: String!) { issueLabels(filter: {name: {eq: $name}}) { nodes { id team { id } } } }"
USER_QUERY = "query User($name: String!) { users(filter: {name: {eq: $name}}) { nodes { id } } }"
CREATE_MUTATION = "mutation Create($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { identifier } } }"


def cell_text(value: object) -> str:
    """A cell's value as the config's maps write it: an empty cell is the empty string."""
    return "" if value is None else str(value)


def short_title(text: str) -> str:
    """The feedback's first line, cut at a word before the title length."""
    line = text.strip().splitlines()[0]
    if len(line) <= TITLE_LENGTH:
        return line
    return line[:TITLE_LENGTH].rsplit(" ", 1)[0] + "…"


def read_groups(sheet: object, sheet_config: dict) -> tuple[dict, dict]:
    """Rows to graduate, grouped, and the issue address each group already has from rows graduated before."""
    columns = sheet_config["columns"]
    groups = {}
    existing = {}
    for number in range(sheet_config["first_row"], sheet.max_row + 1):
        feedback = sheet.cell(number, columns["feedback"]).value
        if feedback is None:
            continue
        group = cell_text(sheet.cell(number, columns["group"]).value).strip()
        address = sheet.cell(number, columns["issue"]).value
        if group and address:
            # One group must point at one issue; two addresses mean the sheet needs fixing by hand.
            if existing.setdefault(group, address) != address:
                raise ValueError(f"Group {group!r} links to both {existing[group]} and {address}")
        if address or cell_text(sheet.cell(number, columns["decision"]).value) != sheet_config["build"]:
            continue
        details = {name: sheet.cell(number, column).value for name, column in sheet_config["details"].items()}
        row = {
            "row": number,
            "feedback": str(feedback),
            "priority": sheet_config["priority"][cell_text(sheet.cell(number, columns["priority"]).value)],
            "owner": sheet_config["owner"][cell_text(sheet.cell(number, columns["owner"]).value)],
            "details": details,
        }
        # An ungrouped row is a group of one, keyed so it cannot meet a typed group name.
        groups.setdefault(group or f"row {number}", []).append(row)
    return groups, existing


def describe(group: str, rows: list[dict]) -> str:
    """The issue body: every row's feedback and details, so the owner can work from the issue alone."""
    parts = [f"From the feedback sheet, {'group ' + repr(group) if len(rows) > 1 else group}."]
    for row in rows:
        quoted = "\n".join(f"> {line}" for line in row["feedback"].splitlines())
        # One tight list per row; an empty detail cell has nothing to say, so it is left out.
        details = "\n".join(
            f"- {name}: {value.strftime('%d %b %Y') if isinstance(value, datetime) else value}"
            for name, value in row["details"].items() if value is not None
        )
        parts.append(f"### Row {row['row']}\n\n{quoted}\n\n{details}")
    return "\n\n".join(parts)


def single(nodes: list[dict], what: str) -> dict:
    """The one node a lookup must find; none or several stops the run."""
    if len(nodes) != 1:
        raise ValueError(f"Linear has {len(nodes)} matches for {what}, not one")
    return nodes[0]


def plan_issue(group: str, rows: list[dict], config: dict) -> dict:
    """The new issue's title, body, priority and owner, refusing a group whose rows name different owners."""
    owners = {row["owner"] for row in rows}
    if len(owners) != 1:
        raise ValueError(f"Rows {[row['row'] for row in rows]} in {group!r} name different owners: {sorted(owners)}")
    # The group takes its most urgent row's priority; Linear numbers urgency from 1.
    priority = min(LINEAR_PRIORITY[config["tracker_priority"][row["priority"]]] for row in rows)
    title = short_title(rows[0]["feedback"]) + (f" (+{len(rows) - 1} similar)" if len(rows) > 1 else "")
    return {"title": title, "description": describe(group, rows), "priority": priority, "owner": owners.pop()}


def main(config_path: Path, workbook_path: Path, dry_run: bool) -> None:
    """Create one issue per group of rows marked for building, then write each issue's address into its rows."""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    sheet_config = config["sheet"]
    load_dotenv(Path(".env"))
    api_key = os.environ["LINEAR_API_KEY"]
    if not dry_run:
        # Opening for writing fails while someone holds the workbook open, so no issue is made that cannot be linked.
        with open(workbook_path, "r+b"):
            pass
    workbook = openpyxl.load_workbook(workbook_path)
    sheet = workbook[sheet_config["tab"]]
    groups, existing = read_groups(sheet, sheet_config)

    project = run_query(api_key, PROJECT_QUERY, {"id": config["linear_project"]})["project"]
    team_id = single(project["teams"]["nodes"], "the project's team")["id"]
    labels = run_query(api_key, LABEL_QUERY, {"name": config["queue_label"]})["issueLabels"]["nodes"]
    # The queue label is the team's own or a workspace label with no team.
    label_id = single([label for label in labels if label["team"] is None or label["team"]["id"] == team_id], f"label {config['queue_label']!r}")["id"]
    user_ids = {}

    addresses = {}
    for group, rows in groups.items():
        if group in existing:
            addresses[group] = existing[group]
            print(f"{group}: rows {[row['row'] for row in rows]} join {existing[group]}")
            continue
        issue = plan_issue(group, rows, config)
        if issue["owner"] not in user_ids:
            user_ids[issue["owner"]] = single(run_query(api_key, USER_QUERY, {"name": issue["owner"]})["users"]["nodes"], f"user {issue['owner']!r}")["id"]
        print(f"{group}: rows {[row['row'] for row in rows]} -> new issue {issue['title']!r}, {issue['owner']}, priority {issue['priority']}")
        if dry_run:
            continue
        created = run_query(api_key, CREATE_MUTATION, {"input": {
            "teamId": team_id, "projectId": project["id"], "title": issue["title"], "description": issue["description"],
            "priority": issue["priority"], "assigneeId": user_ids[issue["owner"]], "labelIds": [label_id],
        }})["issueCreate"]
        if not created["success"]:
            raise RuntimeError(f"Linear did not create the issue for {group!r}")
        addresses[group] = config["issue_url_prefix"] + created["issue"]["identifier"]
        # Printed as made, so a failed save below still leaves every address on screen.
        print(f"   created {addresses[group]}")

    if dry_run or not addresses:
        print(f"{len(groups)} group(s) to graduate; nothing written")
        return
    issue_column = sheet_config["columns"]["issue"]
    for group, rows in groups.items():
        for row in rows:
            sheet.cell(row["row"], issue_column).value = addresses[group]
    workbook.save(workbook_path)
    check = openpyxl.load_workbook(workbook_path)[sheet_config["tab"]]
    for group, rows in groups.items():
        for row in rows:
            print(f"row {row['row']} column {issue_column}: {check.cell(row['row'], issue_column).value}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:] == ["--dry-run"])
