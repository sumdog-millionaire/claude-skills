"""Validate a project's decision records: the DDR register and the ADRs' front matter.

The sync hook runs it before a record edit is pushed to main, so a malformed row never reaches anyone else.
By hand, from the project root:

    python check_records.py docs/ddr/register.csv docs/adr
"""

import csv
import json
import re
import sys
from pathlib import Path

TAXONOMY = json.loads((Path(__file__).resolve().parents[1] / "taxonomy.json").read_text(encoding="utf-8"))
AREA_OF = {sub: area for area, spec in TAXONOMY.items() for sub in spec["sub_areas"]}

# Decisions dated from here must name their alternatives; earlier rows were kept as written
NEW_ROWS_FROM = "2026-10-17"

COLUMNS = "id status layer area sub_area project_taxonomy priority risk built_prototype built_production decided statement why alternatives tracker_issue settled_by supersedes superseded_by adrs".split()
# A register that also holds requirements, conflicts and sources adds a type column and four more
TYPED_COLUMNS = "id type status layer area sub_area project_taxonomy priority risk built_prototype built_production decided statement why alternatives provenance citation tracker_issue settled_by supersedes superseded_by adrs section".split()

BUILT = "yes partial no".split()
UNDECIDED = {"proposed", "in-research", "deferred"}
TAGS = {"area", "sub_area"}

# Each type has its own id shape, its own statuses, and its own required columns
RULES = {
    "decision": {
        "id": r"D\d+",
        "status": "proposed in-research accepted rejected deferred superseded".split(),
        "required": "status layer area sub_area priority risk built_prototype built_production decided statement".split(),
    },
    "requirement": {
        "id": r"REQ-\d+",
        "status": "proposed accepted rejected deferred superseded".split(),
        "required": "status area sub_area priority statement provenance citation".split(),
    },
    "conflict": {
        "id": r"C\d+",
        "status": ["open", "resolved"],
        "required": "status statement why".split(),
    },
    "source": {
        "id": r"[A-Z0-9][A-Z0-9-]*",
        "status": [""],
        "required": "statement provenance".split(),
    },
}

VOCABULARY = {
    "layer": "frontend backend data infra architecture content system".split(),
    "area": list(TAXONOMY),
    "sub_area": list(AREA_OF),
    "priority": "must should could".split(),
    "risk": "high medium low".split(),
    "built_prototype": BUILT,
    "built_production": BUILT,
}
ADR_STATUSES = "proposed accepted deprecated superseded".split()
STATEMENT_LIMIT = 600


def ids(cell: str) -> list[str]:
    """Split a semicolon-separated list, dropping the empties."""
    return [value.strip() for value in cell.split(";") if value.strip()]


def check_tags(where: str, area: str, sub_area: str, project: list[str], project_taxonomy: dict) -> list[str]:
    """Errors in one record's area, sub-area and project taxonomy entries."""
    errors = []
    if area and sub_area in AREA_OF and AREA_OF[sub_area] != area:
        errors.append(f"{where}: sub_area {sub_area!r} belongs to {AREA_OF[sub_area]!r}, not {area!r}")
    for entry in project:
        if entry not in project_taxonomy:
            errors.append(f"{where}: project_taxonomy {entry!r} is not in project_taxonomy.json")
    return errors


def check_register(rows: list[dict[str, str]], project_taxonomy: dict, adr_numbers: set[str]) -> tuple[list[str], list[str]]:
    """Return the register's errors and warnings."""
    errors, warnings = [], []
    known = {row["id"] for row in rows}
    by_id = {row["id"]: row for row in rows}
    if len(known) != len(rows):
        errors.append(f"{len(rows) - len(known)} duplicate id(s)")

    for row in rows:
        this, kind = row["id"], row.get("type", "decision")
        if kind not in RULES:
            errors.append(f"{this}: type is {kind!r}, not one of {', '.join(RULES)}")
            continue
        rule = RULES[kind]
        new = row["decided"] >= NEW_ROWS_FROM

        if not re.fullmatch(rule["id"], this):
            errors.append(f"{this!r}: not a valid id for a {kind}")
        if row["status"] not in rule["status"]:
            errors.append(f"{this}: status is {row['status']!r}, not valid for a {kind}")
        for column in rule["required"]:
            if not row[column]:
                errors.append(f"{this}: {column} is empty on a {kind}")
        for column, allowed in VOCABULARY.items():
            if row[column] and row[column] not in allowed:
                errors.append(f"{this}: {column} is {row[column]!r}, not an allowed value")
        errors += check_tags(this, row["area"], row["sub_area"], ids(row["project_taxonomy"]), project_taxonomy)
        if row["decided"] and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["decided"]):
            errors.append(f"{this}: decided is {row['decided']!r}, not an ISO date")

        if kind == "decision":
            if new and not row["alternatives"]:
                errors.append(f"{this}: alternatives is empty; a decision names the approaches it chose between")
            if (row["status"] == "superseded") != bool(row["superseded_by"]):
                errors.append(f"{this}: status is {row['status']} but superseded_by is {row['superseded_by']!r}")
            if row["status"] in UNDECIDED and not row["settled_by"]:
                errors.append(f"{this}: {row['status']} with nothing named to settle it")

        for column in ("supersedes", "superseded_by", "settled_by"):
            for reference in ids(row[column]):
                # settled_by may name a tracker issue, which is not a row in this file
                if re.fullmatch(r"[A-Z]+-\d+", reference):
                    continue
                if reference not in known:
                    errors.append(f"{this}: {column} names {reference}, which is not in the register")
        for successor in ids(row["superseded_by"]):
            if successor in by_id and this not in ids(by_id[successor]["supersedes"]):
                errors.append(f"{this}: superseded_by names {successor}, which does not list it in supersedes")
        for adr in ids(row["adrs"]):
            if not re.fullmatch(r"ADR-\d{4}", adr) or adr[4:] not in adr_numbers:
                errors.append(f"{this}: adrs names {adr}, which is not an ADR in the folder")
        if len(row["statement"]) > STATEMENT_LIMIT and row["status"] != "superseded":
            warnings.append(f"{this}: statement is {len(row['statement'])} characters; probably several rows sharing one id")
    return errors, warnings


def front_matter(path: Path) -> dict[str, str]:
    """The key: value lines between an ADR's opening --- lines."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    block = text[4:text.index("\n---", 4)]
    return dict(line.split(":", 1) for line in block.splitlines() if ":" in line)


def check_adrs(folder: Path, project_taxonomy: dict) -> list[str]:
    """Errors in the ADRs' front matter."""
    errors = []
    for path in sorted(folder.glob("[0-9][0-9][0-9][0-9]-*.md")):
        meta = {key.strip(): value.strip() for key, value in front_matter(path).items()}
        where = path.name
        if not meta:
            errors.append(f"{where}: no front matter")
            continue
        status = meta.get("status", "").split(" ")[0]
        if status not in ADR_STATUSES:
            errors.append(f"{where}: status is {meta.get('status')!r}, not one of {', '.join(ADR_STATUSES)}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta.get("date", "")):
            errors.append(f"{where}: date is {meta.get('date')!r}, not an ISO date")
        for column in TAGS:
            value = meta.get(column, "")
            if not value:
                errors.append(f"{where}: {column} is missing")
            if value and value not in VOCABULARY[column]:
                errors.append(f"{where}: {column} is {value!r}, not an allowed value")
        errors += check_tags(where, meta.get("area", ""), meta.get("sub_area", ""), ids(meta.get("project_taxonomy", "")), project_taxonomy)
    return errors


def main() -> None:
    register, adr_folder = Path(sys.argv[1]), Path(sys.argv[2])
    project_taxonomy = json.loads((register.parent / "project_taxonomy.json").read_text(encoding="utf-8"))
    # utf-8-sig so the byte-order mark Excel needs does not arrive attached to the first column name
    with register.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames not in (COLUMNS, TYPED_COLUMNS):
            sys.exit(f"register columns are {reader.fieldnames}, expected {COLUMNS}, or with a type column {TYPED_COLUMNS}")
        rows = list(reader)

    adr_numbers = {path.name[:4] for path in adr_folder.glob("[0-9][0-9][0-9][0-9]-*.md")}
    errors, warnings = check_register(rows, project_taxonomy, adr_numbers)
    errors += check_adrs(adr_folder, project_taxonomy)
    for warning in warnings:
        print(f"warning: {warning}")
    if errors:
        print(f"\n{len(errors)} error(s) in {len(rows)} rows and {len(adr_numbers)} ADRs:")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    print(f"{len(rows)} rows and {len(adr_numbers)} ADRs valid, {len(warnings)} warning(s)")


if __name__ == "__main__":
    main()
