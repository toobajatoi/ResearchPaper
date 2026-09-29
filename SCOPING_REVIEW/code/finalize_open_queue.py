import csv
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
OUT = ROOT / "data" / "fulltext" / "oa_attempts" / "queue_final"
OUT.mkdir(parents=True, exist_ok=True)

DUPLICATES = {
    "https://doi.org/10.1145/3640794.3665887": "Duplicate of the included arXiv record 2407.11977.",
    "https://doi.org/10.1145/3817112": "Duplicate of the included arXiv record 2409.02244.",
    "https://doi.org/10.48448/jcss-yq64": "Duplicate of the included arXiv record 2605.07925.",
    "https://openalex.org/W7124513320": "Duplicate of https://doi.org/10.48550/arxiv.2601.10198. The arXiv record is the one read.",
    "https://openalex.org/W7132166895": "Duplicate of https://doi.org/10.31234/osf.io/dyxam_v1.",
    "https://doi.org/10.1145/3773077.3806126": "Duplicate of https://doi.org/10.48550/arxiv.2607.18250. The arXiv record is the one read.",
    "https://openalex.org/W7170224918": "Duplicate of https://doi.org/10.48550/arxiv.2607.18250. The arXiv record is the one read.",
}

rows = list(csv.DictReader(SCREEN.open(encoding="utf-8")))
fields = list(rows[0].keys())
n = 0
for row in rows:
    if row["identifier"] in DUPLICATES and row["decision"] == "retain_for_full_text":
        row["stage"] = "abstract"
        row["decision"] = "exclude_duplicate"
        row["reason"] = DUPLICATES[row["identifier"]]
        n += 1
print("duplicates marked", n)
with SCREEN.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

PDFS = {
    "2607.18250": "https://arxiv.org/pdf/2607.18250",
    "2601.10198": "https://arxiv.org/pdf/2601.10198",
}
for name, url in PDFS.items():
    dest = OUT / f"{name}.pdf"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research-screening"})
        data = urllib.request.urlopen(request, timeout=60).read()
        dest.write_bytes(data)
        print(name, len(data))
    except Exception as error:
        print(name, "ERR", error)
