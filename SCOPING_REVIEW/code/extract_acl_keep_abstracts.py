"""Pull abstracts for the ACL Search 1 title-keeps from the local Anthology file."""

import gzip
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "acl" / "anthology+abstracts.bib.gz"
KEEP = ROOT / "data" / "acl" / "search1_title_keep.txt"
OUT = ROOT / "data" / "acl" / "search1_keep_abstracts.txt"


def field(entry, name):
    match = re.search(
        rf'(?is)\b{name}\s*=\s*"(.+?)"\s*,?\s*(?:\n\s*\w+\s*=|\n\}})',
        entry,
    )
    if not match:
        match = re.search(
            rf"(?is)\b{name}\s*=\s*\{{(.+?)\}}\s*,?\s*(?:\n\s*\w+\s*=|\n\}})",
            entry,
        )
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def anthology_id(url):
    match = re.search(r"aclanthology\.org/([0-9]{4}\.[^/\s]+)/?", url or "")
    return match.group(1) if match else ""


def main():
    wanted = {}
    for line in KEEP.read_text(encoding="utf-8").splitlines():
        if " | " not in line:
            continue
        title, url = line.split(" | ", 1)
        wanted[anthology_id(url)] = title.strip()
    found = {}
    with gzip.open(RAW, "rt", encoding="utf-8", errors="replace") as handle:
        chunk = []
        for line in handle:
            if line.startswith("@") and chunk:
                entry = "".join(chunk)
                chunk = [line]
                url = field(entry, "url")
                key = anthology_id(url)
                if key in wanted:
                    found[key] = {
                        "title": field(entry, "title"),
                        "author": field(entry, "author"),
                        "year": field(entry, "year"),
                        "abstract": field(entry, "abstract"),
                        "doi": field(entry, "doi"),
                        "url": url,
                    }
            else:
                chunk.append(line)
    parts = []
    missing = []
    for key, label in wanted.items():
        row = found.get(key)
        if not row:
            missing.append(key)
            continue
        parts.append(
            f"ID: {key}\nYEAR: {row['year']}\nAUTHORS: {row['author']}\n"
            f"TITLE: {row['title']}\nDOI: {row['doi']}\nURL: {row['url']}\n"
            f"ABSTRACT: {row['abstract']}\n"
        )
    OUT.write_text("\n---\n".join(parts), encoding="utf-8")
    print("wanted", len(wanted), "found", len(found), "missing", missing, "chars", OUT.stat().st_size)


if __name__ == "__main__":
    main()
