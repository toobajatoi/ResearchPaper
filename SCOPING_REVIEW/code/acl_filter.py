"""Filter the public ACL Anthology abstracts file for Search 1 and Search 2.

The Anthology website search is Google Custom Search and is not used as the count.
"""

import gzip
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "acl" / "anthology+abstracts.bib.gz"
OUT = ROOT / "data" / "acl"
URL = "https://aclanthology.org/anthology+abstracts.bib.gz"

A = re.compile(
    r"anthropomorph|human-like|human like|humanlike|human-likeness|human likeness|"
    r"social cues|social presence|computers are social actors|human-machine communication|"
    r"human machine communication",
    re.I,
)
B = re.compile(
    r"large language model|language model|\bLLMs?\b|generative AI|generative model|"
    r"chatbot|conversational AI|conversational agent|dialogue system|dialog system|"
    r"AI assistant|machine-generated|AI-generated|text generation|language technolog",
    re.I,
)
C = re.compile(
    r"\b(Urdu|Hindi|Arabic|Persian|Farsi|Punjabi|Bengali|Bangla|Chinese|Mandarin|"
    r"Cantonese|Japanese|Korean|Spanish|French)\b|multilingual|cross-lingual|"
    r"crosslingual|cross-linguistic|non-English|low-resource|South Asian|Global South",
    re.I,
)
D = re.compile(
    r"honorific|grammatical gender|address form|kinship|politeness|speech act|"
    r"person reference|self-reference|first person|first-person|pronoun",
    re.I,
)


def field(entry, name):
    match = re.search(rf"(?is)\b{name}\s*=\s*[\{{\"](.+?)[\}}\"]\s*,?\s*(?:\n\s*\w+\s*=|\n\}})", entry)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def year_of(entry):
    match = re.search(r"(?im)^\s*year\s*=\s*[\{\"]?(20\d\d)", entry)
    return int(match.group(1)) if match else None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not RAW.exists() or RAW.stat().st_size < 1000000:
        print("downloading", flush=True)
        req = urllib.request.Request(URL, headers={"User-Agent": "HMC-scoping-review"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            RAW.write_bytes(resp.read())
        print("bytes", RAW.stat().st_size, flush=True)
    search1 = []
    search2 = []
    seen = 0
    with gzip.open(RAW, "rt", encoding="utf-8", errors="replace") as handle:
        chunk = []
        for line in handle:
            if line.startswith("@") and chunk:
                entry = "".join(chunk)
                chunk = [line]
                seen += 1
                year = year_of(entry)
                if year is None or year < 2020 or year > 2026:
                    continue
                blob = field(entry, "title") + " " + field(entry, "abstract")
                if not blob.strip():
                    continue
                in_b = bool(B.search(blob))
                if not in_b:
                    continue
                row = {
                    "year": str(year),
                    "title": field(entry, "title"),
                    "url": field(entry, "url"),
                    "booktitle": field(entry, "booktitle"),
                }
                if A.search(blob):
                    search1.append(row)
                if C.search(blob) and (A.search(blob) or D.search(blob)):
                    search2.append(row)
            else:
                chunk.append(line)
    print("entries", seen, "search1", len(search1), "search2", len(search2), flush=True)
    for name, rows in (("search1", search1), ("search2", search2)):
        lines = [f"{i}. ({row['year']}) {row['title']} | {row['url']}" for i, row in enumerate(rows, 1)]
        (OUT / f"{name}_titles.txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
