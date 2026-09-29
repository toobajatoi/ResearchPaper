import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data" / "pubmed" / "retained_abstracts.json").read_text(encoding="utf-8"))
lines = []
for item in data["items"]:
    abstract = (item.get("abstract") or "NO ABSTRACT").replace("\n", " ")
    lines.append(f"PMID {item['pmid']} | {item['year']} | {item['journal']}\n{item['title']}\n{abstract[:900]}\n")
out = ROOT / "data" / "pubmed" / "retained_abstracts.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print(len(data["items"]), out.stat().st_size)
