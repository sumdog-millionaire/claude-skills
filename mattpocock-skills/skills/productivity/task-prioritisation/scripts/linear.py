"""Linear API access shared by the fetch and graduation scripts."""

import json
import urllib.request

API_URL = "https://api.linear.app/graphql"


def run_query(api_key: str, query: str, variables: dict) -> dict:
    """Send one GraphQL query or mutation to Linear and return its data, raising on any error Linear reports."""
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(API_URL, data=body, headers={"Authorization": api_key, "Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        reply = json.load(response)
    if "errors" in reply:
        raise RuntimeError(f"Linear refused the request: {reply['errors']}")
    return reply["data"]
