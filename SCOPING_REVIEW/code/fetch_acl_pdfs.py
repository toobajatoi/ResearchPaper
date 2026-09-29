import urllib.request
from pathlib import Path

IDS = [
    "2025.sicon-1.10",
    "2025.emnlp-main.164",
    "2025.emnlp-main.1508",
    "2025.coling-main.239",
    "2024.findings-emnlp.567",
    "2023.ranlp-1.18",
    "2023.emnlp-main.290",
    "2022.emnlp-main.215",
    "2021.naacl-main.61",
    "2021.gebnlp-1.4",
    "2026.findings-eacl.4",
    "2026.clpsych-1.26",
    "2026.acl-long.241",
    "2025.findings-acl.328",
    "2025.findings-acl.1185",
    "2025.acl-long.1261",
    "2024.sigdial-1.21",
    "2024.lrec-main.1166",
]

OUT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts" / "queue_acl_pdf"
OUT.mkdir(parents=True, exist_ok=True)

for anthology_id in IDS:
    dest = OUT / f"{anthology_id}.pdf"
    if dest.exists() and dest.stat().st_size > 10000:
        print(anthology_id, "have", dest.stat().st_size)
        continue
    url = f"https://aclanthology.org/{anthology_id}.pdf"
    try:
        request = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 research-screening"}
        )
        data = urllib.request.urlopen(request, timeout=60).read()
        dest.write_bytes(data)
        print(anthology_id, "pdf", len(data))
    except Exception as error:
        print(anthology_id, "ERR", error)
