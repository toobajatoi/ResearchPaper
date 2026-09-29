"""Extract text from the two downloaded open PDFs. Output stays in the gitignored folder."""

import fitz
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts"
for name in ("gao_plos.pdf", "ollier_frontiers.pdf"):
    doc = fitz.open(OUT / name)
    parts = []
    for page in doc:
        parts.append(page.get_text())
    text = "\n".join(parts)
    path = OUT / (name.replace(".pdf", ".txt"))
    path.write_text(text, encoding="utf-8")
    print(name, "pages", doc.page_count, "chars", len(text))
