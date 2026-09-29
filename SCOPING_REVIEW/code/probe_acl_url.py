"""Show how one known Anthology id is stored in the local bib file."""

import gzip
import re
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "acl" / "anthology+abstracts.bib.gz"
NEEDLE = "2025.acl-long.1259"
shown = 0
with gzip.open(RAW, "rt", encoding="utf-8", errors="replace") as handle:
    chunk = []
    for line in handle:
        if line.startswith("@") and chunk:
            entry = "".join(chunk)
            chunk = [line]
            if NEEDLE in entry:
                print(entry[:1500])
                print("---END---")
                shown += 1
                if shown >= 1:
                    break
        else:
            chunk.append(line)
print("shown", shown)
