"""Download the 15 HMC papers retained for full-text reading."""

import csv
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
OUT = ROOT / "data" / "fulltext" / "hmc"
OUT.mkdir(parents=True, exist_ok=True)


def pdf_url(identifier):
    parts = [part.strip() for part in identifier.split("|")]
    for part in parts:
        if part.endswith(".pdf"):
            return part
    return ""


def main():
    with SCREEN.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    kept = [row for row in rows if row["decision"] == "retain_for_full_text"]
    for row in kept:
        url = pdf_url(row["identifier"])
        dest = OUT / f"hmc_{int(row['record_number']):03d}.pdf"
        if dest.exists() and dest.stat().st_size > 1000:
            print("exists", dest.name)
            continue
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                "Accept": "application/pdf,application/xhtml+xml",
                "Referer": "https://stars.library.ucf.edu/hmc/",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            dest.write_bytes(data)
            print(dest.name, len(data), url)
        except Exception as exc:
            print("FAIL", row["record_number"], type(exc).__name__, exc)
        time.sleep(0.4)


if __name__ == "__main__":
    main()
