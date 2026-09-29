"""Download arXiv HTML for the four openly available full texts."""

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "fulltext" / "arxiv"
OUT.mkdir(parents=True, exist_ok=True)

PAPERS = {
    "2502.09870": "devrio_taxonomy",
    "2502.07077": "ibrahim_multiturn",
    "2502.14019": "cheng_dehumanizing",
    "2305.16367": "shanahan_roleplay",
}


def main():
    for arxiv_id, name in PAPERS.items():
        url = f"https://arxiv.org/html/{arxiv_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
        dest = OUT / f"{name}.html"
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
            dest.write_bytes(data)
            print(name, resp.status, len(data), flush=True)
        except Exception as exc:
            print("FAIL", name, type(exc).__name__, exc, flush=True)


if __name__ == "__main__":
    main()
