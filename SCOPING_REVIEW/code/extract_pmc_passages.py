"""Pull methods and cue-related passages from downloaded PMC XML."""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PMC = ROOT / "data" / "fulltext" / "pmc"
AVAIL = ROOT / "data" / "fulltext" / "availability.json"
OUT = ROOT / "data" / "fulltext" / "passages"
OUT.mkdir(parents=True, exist_ok=True)

TERMS = re.compile(
    r"anthropomorph|human-like|humanlike|empath|social presence|first-person|first person|"
    r"pronoun|honorific|politeness|kinship|self-refer|sycophan|role play|language|urdu|hindi|"
    r"arabic|chinese|korean|spanish|french|multilingual|cue",
    re.I,
)


def local(tag):
    return tag.rsplit("}", 1)[-1]


def text_of(node):
    return " ".join(part.strip() for part in node.itertext() if part and part.strip())


def main():
    by_pmc = {row["pmcid"]: row for row in json.loads(AVAIL.read_text(encoding="utf-8")) if row.get("pmcid")}
    for path in sorted(PMC.glob("*.xml")):
        pmcid = path.stem
        meta = by_pmc.get(pmcid, {})
        root = ET.parse(path).getroot()
        sections = []
        for sec in root.iter():
            if local(sec.tag) != "sec":
                continue
            title_node = None
            for child in list(sec):
                if local(child.tag) == "title":
                    title_node = child
                    break
            title = text_of(title_node) if title_node is not None else ""
            body = text_of(sec)
            if title or body:
                sections.append((title, body))
        lines = [
            f"PMCID {pmcid}",
            f"PMID {meta.get('pmid','')}",
            f"DOI {meta.get('doi','')}",
            f"TITLE {meta.get('title','')}",
            "",
            "SECTIONS: " + " | ".join(title for title, _ in sections if title),
            "",
        ]
        for title, body in sections:
            if re.search(r"method|material|procedure|result|finding|discussion", title, re.I):
                lines.append(f"## {title}")
                lines.append(body[:3500])
                lines.append("")
        lines.append("## CUE PASSAGES")
        kept = 0
        for title, body in sections:
            for sentence in re.split(r"(?<=[.?!])\s+", body):
                if TERMS.search(sentence) and len(sentence) > 40:
                    lines.append(f"- [{title}] {sentence[:500]}")
                    kept += 1
                    if kept >= 25:
                        break
            if kept >= 25:
                break
        (OUT / f"{pmcid}.txt").write_text("\n".join(lines), encoding="utf-8")
    print("passages", len(list(OUT.glob('*.txt'))))


if __name__ == "__main__":
    main()
