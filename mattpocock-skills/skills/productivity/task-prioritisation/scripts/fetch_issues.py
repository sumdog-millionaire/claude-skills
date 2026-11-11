"""Fetch every issue of one Linear project, open or closed, and save them as the issues file the table is built from.

Run from the project root, whose .env holds LINEAR_API_KEY:
    python fetch_issues.py docs/agents/task-prioritisation.json
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

API_URL = "https://api.linear.app/graphql"
QUERY = """
query ProjectIssues($project: String!, $after: String) {
  project(id: $project) {
    issues(first: 100, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes {
        identifier
        title
        priorityLabel
        completedAt
        state { name type }
        assignee { name }
        projectMilestone { name }
        labels(first: 100) { pageInfo { hasNextPage } nodes { name } }
      }
    }
  }
}
"""


def run_query(api_key: str, variables: dict) -> dict:
    """Send the query to Linear and return its data, raising on any error Linear reports."""
    body = json.dumps({"query": QUERY, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(API_URL, data=body, headers={"Authorization": api_key, "Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        reply = json.load(response)
    if "errors" in reply:
        raise RuntimeError(f"Linear refused the query: {reply['errors']}")
    return reply["data"]


def fetch_issues(api_key: str, project: str) -> list[dict]:
    """Every issue in the project, open or closed, following every page; the build chooses what to show."""
    issues = []
    after = None
    while True:
        data = run_query(api_key, {"project": project, "after": after})
        if data["project"] is None:
            raise ValueError(f"Linear has no project {project!r}")
        page = data["project"]["issues"]
        for node in page["nodes"]:
            if node["labels"]["pageInfo"]["hasNextPage"]:
                raise ValueError(f"{node['identifier']} has more than 100 labels, so its list would be cut short")
            issues.append({
                "id": node["identifier"],
                "title": node["title"],
                "status": node["state"]["name"],
                "status_type": node["state"]["type"],
                "completed_at": node["completedAt"],
                # An unassigned issue or one outside every milestone has null there.
                "assignee": node["assignee"]["name"] if node["assignee"] else None,
                "priority": node["priorityLabel"],
                "milestone": node["projectMilestone"]["name"] if node["projectMilestone"] else None,
                "labels": [label["name"] for label in node["labels"]["nodes"]],
            })
        if not page["pageInfo"]["hasNextPage"]:
            return issues
        after = page["pageInfo"]["endCursor"]


def main(config_path: Path) -> None:
    """Write every issue in the project to issues.json in the config's output folder."""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    load_dotenv(Path(".env"))
    issues = fetch_issues(os.environ["LINEAR_API_KEY"], config["linear_project"])
    output = Path(config["output_dir"]) / "issues.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(issues, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(issues)} issues written to {output}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
