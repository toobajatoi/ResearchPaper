import csv
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / "data" / "author_verification_sample.csv").open(encoding="utf-8")))
out = root / "data" / "fulltext" / "oa_attempts" / "blank_checks.txt"
lines = []
for i, row in enumerate(rows, 1):
    if (row.get("author_checked") or "").strip():
        continue
    title = (row.get("title") or "").replace("\n", " ")
    reason = (row.get("reason") or "").replace("\n", " ")
    lines.append(f"{i}\t{row['decision']}\t{title[:140]}\t{reason[:220]}")
out.write_text("\n".join(lines), encoding="utf-8")
print(len(lines))
