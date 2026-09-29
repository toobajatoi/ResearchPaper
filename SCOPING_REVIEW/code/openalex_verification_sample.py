"""Sample the first 80 OpenAlex abstract decisions for the author to check.

Every full-text keep in that set, plus a fixed 10 percent of the exclusions.
author_checked stays blank. This script does not record a verification.
"""

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
OUT = ROOT / "data" / "author_verification_openalex.csv"
SEED = 20260929


def main():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    openalex = [row for row in rows if row["source"].startswith("OpenAlex")]
    decided = [row for row in openalex if "Abstract not yet read" not in row["reason"]]
    first = decided[:80]
    keeps = [row for row in first if row["decision"] == "retain_for_full_text"]
    exclusions = [row for row in first if row["decision"].startswith("exclude")]
    sample_n = max(1, round(len(exclusions) * 0.10))
    rng = random.Random(SEED)
    sample = rng.sample(exclusions, sample_n)
    out_rows = [("full_text_keep", row) for row in keeps]
    out_rows.extend(("exclusion_sample", row) for row in sample)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "check_type",
                "source",
                "identifier",
                "year",
                "title",
                "decision",
                "reason",
                "author_checked",
                "author_note",
            ],
        )
        writer.writeheader()
        for kind, row in out_rows:
            writer.writerow(
                {
                    "check_type": kind,
                    "source": row["source"],
                    "identifier": row["identifier"],
                    "year": row["year"],
                    "title": row["title"],
                    "decision": row["decision"],
                    "reason": row["reason"],
                    "author_checked": "",
                    "author_note": "",
                }
            )
    print("first80", len(first), "keeps", len(keeps), "exclusions", len(exclusions), "sample", sample_n)


if __name__ == "__main__":
    main()
