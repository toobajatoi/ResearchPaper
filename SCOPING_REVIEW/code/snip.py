"""Print a window of plain text around the first match of a phrase."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    pmcid = sys.argv[1]
    phrase = sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    path = ROOT / "data" / "fulltext" / "pmc" / f"{pmcid}.xml"
    text = " ".join(part.strip() for part in ET.parse(path).getroot().itertext() if part and part.strip())
    idx = text.lower().find(phrase.lower())
    print("idx", idx, "len", len(text))
    if idx < 0:
        return
    start = max(0, idx - 200)
    print(text[start : idx + width])


if __name__ == "__main__":
    main()
