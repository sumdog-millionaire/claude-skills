"""Turn every open, assigned feedback row with no linked issue into a Linear issue and write each issue's link back into its rows.

Run from the project root, whose .env holds LINEAR_API_KEY:
    python graduate.py docs/agents/task-prioritisation.json "<feedback workbook>" [--groups <groups.json>] [--dry-run]

--dry-run checks every lookup and prints each row and the issues it would create, creating and writing nothing; it can read a copy of the workbook.
--groups names a JSON file {"new": [{"title": "...", "milestone": "<name or null>", "rows": [row, ...]}, ...], "existing": {"ENG-134": {"milestone": "<name or null>", "rows": [row, ...]}}}: each "new" group is one issue, each "existing" entry
links its rows to that issue (or, when it is in progress, to a new issue in that milestone related to it), and a row in neither is an issue of its own.
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import openpyxl
from dotenv import load_dotenv

# A sibling module: Python puts this script's folder on the import path when it runs the script.
from linear import run_query

LINEAR_PRIORITY = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4}
NO_PRIORITY = 0
TITLE_LENGTH = 80
PROJECT_QUERY = "query Project($id: String!) { project(id: $id) { id teams { nodes { id } } projectMilestones { nodes { id name } } } }"
LABEL_QUERY = "query Label($name: String!) { issueLabels(filter: {name: {eq: $name}}) { nodes { id team { id } } } }"
ISSUE_QUERY = "query Issue($id: String!) { issue(id: $id) { id identifier state { type } } }"
RELATE_MUTATION = "mutation Relate($input: IssueRelationCreateInput!) { issueRelationCreate(input: $input) { success } }"
USER_QUERY = "query User($name: String!) { users(filter: {name: {eq: $name}}) { nodes { id } } }"
CREATE_MUTATION = "mutation Create($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier } } }"


def cell_text(value: object) -> str:
    """A cell's value as the config's maps write it: an empty cell is the empty string."""
    return "" if value is None else str(value).strip()


def short_title(text: str) -> str:
    """The feedback's first line, cut at a word before the title length."""
    line = text.strip().splitlines()[0]
    if len(line) <= TITLE_LENGTH:
        return line
    return line[:TITLE_LENGTH].rsplit(" ", 1)[0] + "…"


def read_rows(sheet: object, sheet_config: dict) -> dict[int, dict]:
    """Every row with feedback, an owner, no linked issue and a status the config does not call closed, keyed by row number."""
    columns = sheet_config["columns"]
    rows = {}
    for number in range(sheet_config["first_row"], sheet.max_row + 1):
        feedback = sheet.cell(number, columns["feedback"]).value
        owner = cell_text(sheet.cell(number, columns["owner"]).value)
        if feedback is None or not owner or sheet.cell(number, columns["issue"]).value:
            continue
        if cell_text(sheet.cell(number, columns["status"]).value) in sheet_config["closed"]:
            continue
        rows[number] = {
            "row": number,
            "feedback": str(feedback),
            "priority": sheet_config["priority"][cell_text(sheet.cell(number, columns["priority"]).value)],
            "owner": sheet_config["owner"][owner],
            "details": {name: sheet.cell(number, column).value for name, column in sheet_config["details"].items()},
        }
    return rows


def group_rows(rows: dict[int, dict], groups: dict) -> tuple[list[tuple[list[dict], str | None, str]], dict[str, tuple[list[dict], str | None]]]:
    """New issues as rows, milestone name and title (the agreed groups, then every row no group names, alone) and rows joining existing issues."""
    grouped = [number for group in [*groups["new"], *groups["existing"].values()] for number in group["rows"]]
    for number in grouped:
        if number not in rows:
            raise ValueError(f"Row {number} is in a group but is not an open, assigned row without an issue")
    if len(grouped) != len(set(grouped)):
        raise ValueError(f"A row is in more than one group: {groups}")
    new = [([rows[number] for number in group["rows"]], group["milestone"], group["title"]) for group in groups["new"]]
    new += [([row], None, short_title(row["feedback"])) for number, row in rows.items() if number not in grouped]
    existing = {identifier: ([rows[number] for number in group["rows"]], group["milestone"]) for identifier, group in groups["existing"].items()}
    return new, existing


def describe(rows: list[dict]) -> str:
    """The issue body: every row's feedback and details, so the owner can work from the issue alone."""
    parts = [f"From the feedback sheet, row{'s' if len(rows) > 1 else ''} {', '.join(str(row['row']) for row in rows)}."]
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


def plan_issue(rows: list[dict], title: str, config: dict) -> dict:
    """The new issue's body, priority and owner beside its title, refusing a group whose rows name different owners."""
    owners = {row["owner"] for row in rows}
    if len(owners) != 1:
        raise ValueError(f"Rows {[row['row'] for row in rows]} name different owners: {sorted(owners)}")
    # The group takes its most urgent row's priority; Linear numbers urgency from 1 and 0 is none.
    priorities = [LINEAR_PRIORITY[config["tracker_priority"][row["priority"]]] for row in rows if row["priority"] is not None]
    return {"title": title, "description": describe(rows), "priority": min(priorities, default=NO_PRIORITY), "owner": owners.pop()}


def main(config_path: Path, workbook_path: Path, groups_path: Path | None, dry_run: bool) -> None:
    """Create one issue per group of open rows without an issue, then write each issue's address into its rows."""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    sheet_config = config["sheet"]
    groups = json.loads(groups_path.read_text(encoding="utf-8")) if groups_path else {"new": [], "existing": {}}
    load_dotenv(Path(".env"))
    api_key = os.environ["LINEAR_API_KEY"]
    if not dry_run:
        # Opening for writing fails while someone holds the workbook open, so no issue is made that cannot be linked.
        with open(workbook_path, "r+b"):
            pass
    workbook = openpyxl.load_workbook(workbook_path)
    sheet = workbook[sheet_config["tab"]]
    rows = read_rows(sheet, sheet_config)
    for row in rows.values():
        print(f"row {row['row']}: {row['owner']}, {row['priority'] or 'no priority'}: {short_title(row['feedback'])}")
    new, existing = group_rows(rows, groups)
    issues = [(issue_rows, None, milestone, title) for issue_rows, milestone, title in new]

    addresses = []
    for identifier, (issue_rows, milestone) in existing.items():
        # Linear accepts an identifier as the id and raises when no issue has it.
        found = run_query(api_key, ISSUE_QUERY, {"id": identifier})["issue"]
        # Work already under way is not widened: its rows get a new issue in the planned milestone, related to it.
        if found["state"]["type"] == "started":
            issues.append((issue_rows, found, milestone, short_title(issue_rows[0]["feedback"])))
            continue
        addresses.append((issue_rows, config["issue_url_prefix"] + found["identifier"]))
        print(f"rows {[row['row'] for row in issue_rows]} -> existing issue {found['identifier']}")

    project = run_query(api_key, PROJECT_QUERY, {"id": config["linear_project"]})["project"]
    team_id = single(project["teams"]["nodes"], "the project's team")["id"]
    labels = run_query(api_key, LABEL_QUERY, {"name": config["queue_label"]})["issueLabels"]["nodes"]
    # The queue label is the team's own or a workspace label with no team.
    label_id = single([label for label in labels if label["team"] is None or label["team"]["id"] == team_id], f"label {config['queue_label']!r}")["id"]
    milestone_ids = {milestone["name"]: milestone["id"] for milestone in project["projectMilestones"]["nodes"]}
    user_ids = {}

    for issue_rows, related, milestone, title in issues:
        issue = plan_issue(issue_rows, title, config)
        # A name the project has no milestone for raises here, before anything is created.
        milestone_id = milestone_ids[milestone] if milestone is not None else None
        if related is not None:
            issue["description"] += f"\n\nRelated to {related['identifier']}, which was already in progress when these rows were graduated."
        if issue["owner"] not in user_ids:
            user_ids[issue["owner"]] = single(run_query(api_key, USER_QUERY, {"name": issue["owner"]})["users"]["nodes"], f"user {issue['owner']!r}")["id"]
        relation = f", related to in-progress {related['identifier']}" if related is not None else ""
        print(f"rows {[row['row'] for row in issue_rows]} -> new issue {issue['title']!r}, {issue['owner']}, priority {issue['priority']}, milestone {milestone}{relation}")
        if dry_run:
            continue
        created = run_query(api_key, CREATE_MUTATION, {"input": {
            "teamId": team_id, "projectId": project["id"], "projectMilestoneId": milestone_id, "title": issue["title"],
            "description": issue["description"], "priority": issue["priority"], "assigneeId": user_ids[issue["owner"]], "labelIds": [label_id],
        }})["issueCreate"]
        if not created["success"]:
            raise RuntimeError(f"Linear did not create the issue for rows {[row['row'] for row in issue_rows]}")
        if related is not None:
            relation_made = run_query(api_key, RELATE_MUTATION, {"input": {"issueId": created["issue"]["id"], "relatedIssueId": related["id"], "type": "related"}})
            if not relation_made["issueRelationCreate"]["success"]:
                raise RuntimeError(f"Linear did not relate {created['issue']['identifier']} to {related['identifier']}")
        address = config["issue_url_prefix"] + created["issue"]["identifier"]
        addresses.append((issue_rows, address))
        # Printed as made, so a failed save below still leaves every address on screen.
        print(f"   created {address}")

    if dry_run or not addresses:
        print(f"{len(issues)} issue(s) to create and {len(addresses)} existing issue(s) to link, from {len(rows)} row(s); nothing written")
        return
    issue_column = sheet_config["columns"]["issue"]
    for issue_rows, address in addresses:
        for row in issue_rows:
            sheet.cell(row["row"], issue_column).value = address
    workbook.save(workbook_path)
    check = openpyxl.load_workbook(workbook_path)[sheet_config["tab"]]
    for issue_rows, _ in addresses:
        for row in issue_rows:
            print(f"row {row['row']} column {issue_column}: {check.cell(row['row'], issue_column).value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("config", type=Path)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--groups", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    main(arguments.config, arguments.workbook, arguments.groups, arguments.dry_run)
