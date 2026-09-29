"""Print selected section titles and short bodies from PMC XML."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def local(tag):
    return tag.rsplit("}", 1)[-1]


def text_of(node):
    return " ".join(part.strip() for part in node.itertext() if part and part.strip())


def main():
    pmcid = sys.argv[1]
    needles = [item.lower() for item in sys.argv[2:]]
    path = ROOT / "data" / "fulltext" / "pmc" / f"{pmcid}.xml"
    root = ET.parse(path).getroot()
    for sec in root.iter():
        if local(sec.tag) != "sec":
            continue
        title = ""
        for child in list(sec):
            if local(child.tag) == "title":
                title = text_of(child)
                break
        body = text_of(sec)
        hay = (title + " " + body[:500]).lower()
        if any(needle in hay for needle in needles):
            print("##", title[:180])
            print(body[:1800])
            print()


if __name__ == "__main__":
    main()
