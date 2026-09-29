import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data" / "pubmed" / "search1_summaries.json").read_text(encoding="utf-8"))
out = ROOT / "data" / "pubmed" / "titles.txt"
lines = []
for i, item in enumerate(data["items"], start=1):
    title = (item.get("title") or "").replace("\n", " ")
    lines.append(f"{i}\t{item.get('pubdate','')}\t{item.get('pmid','')}\t{title}")
out.write_text("\n".join(lines), encoding="utf-8")
print(len(lines))
