"""Build the task prioritisation table: every open issue and every issue completed in the last week, as one local HTML page.

Run from the project root:
    python build_table.py docs/agents/task-prioritisation.json <output_dir>/issues.json
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TEMPLATE = Path(__file__).with_name("template.html")
DATA_MARKER = "/*DATA*/null"
OPEN_STATE_TYPES = ("triage", "backlog", "unstarted", "started")
CLOSED_STATE_TYPES = ("canceled", "duplicate")
RECENT_DAYS = 7


def is_shown(issue: dict, since: datetime) -> bool:
    """Whether the table shows an issue: open, or completed since the cut-off; never cancelled or duplicate."""
    kind = issue["status_type"]
    if kind in OPEN_STATE_TYPES:
        return True
    if kind == "completed":
        return datetime.fromisoformat(issue["completed_at"]) >= since
    if kind in CLOSED_STATE_TYPES:
        return False
    raise ValueError(f"{issue['id']} has status type {kind!r}, which the build does not know")


def read_issues(config: dict, issues_path: Path) -> list[dict]:
    """The issues the table shows, in the table's words, each with its address."""
    since = datetime.now(timezone.utc) - timedelta(days=RECENT_DAYS)
    issues = []
    for issue in json.loads(issues_path.read_text(encoding="utf-8")):
        if not is_shown(issue, since):
            continue
        completed = datetime.fromisoformat(issue["completed_at"]).strftime("%d %b") if issue["completed_at"] else ""
        issues.append({
            "id": issue["id"],
            "title": issue["title"],
            "status": config["issue_status"][issue["status"]],
            "priority": config["issue_priority"][issue["priority"]],
            "owner": issue["assignee"],
            "milestone": issue["milestone"],
            "completed": completed,
            "queue": config["queue_label"] in issue["labels"],
            "url": config["issue_url_prefix"] + issue["id"],
        })
    return issues


def main(config_path: Path, issues_path: Path) -> None:
    """Write the table page from the config and the saved issues."""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    template = TEMPLATE.read_text(encoding="utf-8")
    if DATA_MARKER not in template:
        raise ValueError(f"{TEMPLATE} has lost its data marker {DATA_MARKER}")
    issues = read_issues(config, issues_path)
    data = {
        "refreshed": datetime.now().strftime("%d %b %Y, %H:%M"),
        "queueLabel": config["queue_label"],
        # Everyone an issue can be given to: every shown issue's assignee.
        "owners": sorted({issue["owner"] for issue in issues if issue["owner"]}),
        "issues": issues,
    }
    # A "</" inside the data would close the page's script tag early.
    text = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    output = Path(config["output_dir"]) / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template.replace(DATA_MARKER, text), encoding="utf-8")
    print(f"{len(issues)} issues written to {output}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
