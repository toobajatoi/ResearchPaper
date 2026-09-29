"""List every inclusion and a fixed 10 percent sample of exclusions for the author to check.

The author_checked column is left blank. This script does not record a verification.
"""

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
OUT = ROOT / "data" / "author_verification_sample.csv"
SEED = 20260929


def main():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    includes = [row for row in rows if row["decision"] == "include"]
    exclusions = [row for row in rows if row["decision"].startswith("exclude")]
    sample_n = max(1, round(len(exclusions) * 0.10))
    rng = random.Random(SEED)
    sample = rng.sample(exclusions, sample_n)
    out_rows = []
    for row in includes:
        out_rows.append(("included_study", row))
    for row in sample:
        out_rows.append(("exclusion_sample", row))
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
    print("includes", len(includes), "exclusions", len(exclusions), "sample", sample_n)


if __name__ == "__main__":
    main()
