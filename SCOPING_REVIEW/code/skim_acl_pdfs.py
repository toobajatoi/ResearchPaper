import pymupdf
from pathlib import Path

folder = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts" / "queue_acl_pdf"
out = folder.parent / "queue_acl_skim.txt"
parts = []
for pdf in sorted(folder.glob("*.pdf")):
    doc = pymupdf.open(pdf)
    pages = []
    for i, page in enumerate(doc):
        if i > 2 and i < doc.page_count - 2:
            continue
        pages.append(page.get_text("text"))
    text = "\n".join(pages)
    text = " ".join(text.split())
    parts.append(f"\n\n===== {pdf.stem} pages={doc.page_count} =====\n{text[:3500]}\n---ENDHEAD---\n{text[-1800:]}")
    doc.close()
out.write_text("\n".join(parts), encoding="utf-8")
print("wrote", out, "chars", out.stat().st_size)
