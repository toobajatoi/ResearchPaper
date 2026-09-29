"""Download three open full texts that the abstracts already kept. Save under the gitignored folder."""

import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts"
OUT.mkdir(parents=True, exist_ok=True)
UA = "HMC-scoping-review"
URLS = {
    "gao_plos.pdf": "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0338524&type=printable",
    "ollier_frontiers.pdf": "https://www.frontiersin.org/articles/10.3389/fpubh.2021.691595/pdf",
    "ollier_epmc.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8767023/fullTextXML",
    "gao_epmc.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13405109/fullTextXML",
    "shen_epmc.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13507331/fullTextXML",
}


def main():
    for name, url in URLS.items():
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        path = OUT / name
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = resp.read()
            path.write_bytes(body)
            print(name, resp.status, len(body), body[:5], flush=True)
        except Exception as exc:
            print(name, type(exc).__name__, exc, flush=True)


if __name__ == "__main__":
    main()
