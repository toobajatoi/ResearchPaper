"""Check that each PMC XML title matches the PubMed queue title."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def local(tag):
    return tag.rsplit("}", 1)[-1]


def norm(text):
    return " ".join(text.lower().replace("\ufffd", "").split())


def main():
    avail = json.loads((ROOT / "data" / "fulltext" / "availability.json").read_text(encoding="utf-8"))
    missing = []
    mismatch = []
    ok = 0
    for meta in avail:
        pmcid = meta.get("pmcid") or ""
        if not pmcid:
            continue
        path = ROOT / "data" / "fulltext" / "pmc" / f"{pmcid}.xml"
        if not path.exists():
            missing.append(pmcid)
            continue
        title = ""
        for el in ET.parse(path).getroot().iter():
            if local(el.tag) == "article-title":
                title = " ".join(el.itertext()).strip()
                break
        a = norm(meta["title"])
        b = norm(title)
        if a[:40] in b or b[:40] in a:
            ok += 1
        else:
            mismatch.append((meta["pmid"], pmcid, meta["title"], title))
    print("ok", ok, "missing", missing, "mismatch", len(mismatch))
    for pmid, pmcid, queue, xml_title in mismatch:
        print("---")
        print(pmid, pmcid)
        print("Q", queue)
        print("X", xml_title)


if __name__ == "__main__":
    main()
