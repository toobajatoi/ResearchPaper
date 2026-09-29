"""Try publisher URLs for papers that have no PMCID. Record HTTP status. Save only 200 responses."""

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "fulltext" / "oa_attempts"
OUT.mkdir(parents=True, exist_ok=True)

CANDIDATES = [
    ("42463863", "https://www.nature.com/articles/s41598-026-62696-9"),
    ("40694494", "https://www.tandfonline.com/doi/pdf/10.1080/15265161.2025.2526734?download=true"),
    ("41548427", "https://www.sciencedirect.com/science/article/pii/S2352250X25002763/pdfft"),
    ("40286349", "https://www.sciencedirect.com/science/article/pii/S000169182500349X/pdfft"),
    ("40810905", "https://link.springer.com/content/pdf/10.1007/s00345-025-05872-2.pdf"),
    ("37938776", "https://www.nature.com/articles/s41586-023-06647-8.pdf"),
    ("37938776b", "https://www.nature.com/articles/s41586-023-06647-8"),
    ("38428201", "https://www.sciencedirect.com/science/article/pii/S1386505624000480/pdfft"),
]


def main():
    for name, url in CANDIDATES:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/html,application/pdf",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                ctype = resp.headers.get("Content-Type", "")
                dest = OUT / f"{name}.bin"
                dest.write_bytes(data)
                print(name, resp.status, ctype, len(data), flush=True)
        except Exception as exc:
            print("FAIL", name, type(exc).__name__, exc, flush=True)


if __name__ == "__main__":
    main()
