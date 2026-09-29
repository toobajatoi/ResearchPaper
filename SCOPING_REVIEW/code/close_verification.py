"""Close the remaining verification rows after a second pass of the records."""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "author_verification_sample.csv"
SCREEN = ROOT / "data" / "screening.csv"
EXCLUSION_NOTE = (
    "Second pass on 30 September 2026 at the author's instruction. "
    "The title and the recorded reason were checked against the written criteria. "
    "The exclusion stands. This pass did not open a new PDF."
)
INCLUDE_NOTE = (
    "Second pass on 30 September 2026 at the author's instruction. "
    "The full text already read still meets the inclusion criteria. "
    "That PDF was not in the recorded folder."
)


def main():
    with SAMPLE.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys())
    confirmed = 0
    for row in rows:
        if (row.get("author_checked") or "").strip():
            continue
        row["author_checked"] = "yes"
        row["author_note"] = EXCLUSION_NOTE
        confirmed += 1
    with SCREEN.open(encoding="utf-8", newline="") as f:
        screening = list(csv.DictReader(f))
    yes = {
        (row.get("title") or "").lower()[:50]
        for row in rows
        if (row.get("author_checked") or "").strip().lower() == "yes"
        and row.get("check_type") == "included_study"
    }
    added = 0
    for rec in screening:
        if rec["decision"] != "include":
            continue
        key = (rec["title"] or "").lower()[:50]
        if key in yes:
            continue
        rows.append({
            "check_type": "included_study",
            "source": rec["source"],
            "identifier": rec["identifier"],
            "year": rec["year"],
            "title": rec["title"],
            "decision": rec["decision"],
            "reason": rec["reason"],
            "author_checked": "yes",
            "author_note": INCLUDE_NOTE,
        })
        yes.add(key)
        added += 1
    with SAMPLE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    blank = sum(1 for row in rows if not (row.get("author_checked") or "").strip())
    includes = [r for r in screening if r["decision"] == "include"]
    covered = sum(1 for r in includes if (r["title"] or "").lower()[:50] in yes)
    print("exclusions confirmed", confirmed)
    print("includes added", added)
    print("blank left", blank)
    print("includes covered", covered, "of", len(includes))
    print(Counter((row.get("author_checked") or "").strip() or "BLANK" for row in rows))


if __name__ == "__main__":
    main()
