import html
import re
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

OUT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts" / "queue_acl_abstracts.txt"


def strip_tags(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    chunks = []
    for anthology_id in IDS:
        url = f"https://aclanthology.org/{anthology_id}/"
        try:
            request = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 research-screening"}
            )
            raw = urllib.request.urlopen(request, timeout=40).read().decode("utf-8", "replace")
            abstract = re.search(
                r'<div class="card-body acl-abstract">(.*?)</div>', raw, re.S
            )
            if not abstract:
                abstract = re.search(r'id="abstract".*?<span>(.*?)</span>', raw, re.S)
            title = re.search(r'<h2 id="title">(.*?)</h2>', raw, re.S)
            abstract_text = strip_tags(abstract.group(1)) if abstract else "NO ABSTRACT"
            title_text = strip_tags(title.group(1)) if title else ""
            chunks.append(
                f"=== {anthology_id} ===\nTITLE: {title_text}\nABSTRACT: {abstract_text}\n"
            )
            print(anthology_id, "ok", len(abstract_text))
        except Exception as error:
            chunks.append(f"=== {anthology_id} ===\nERROR: {error}\n")
            print(anthology_id, "ERR", error)
    OUT.write_text("\n".join(chunks), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
