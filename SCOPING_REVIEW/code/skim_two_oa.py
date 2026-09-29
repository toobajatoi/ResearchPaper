import fitz
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts" / "queue_user_blocked"
for name in ("ijfmr_banking.pdf", "xie.pdf"):
    doc = fitz.open(ROOT / name)
    print("====", name, "pages", doc.page_count)
    text = "\n".join(page.get_text() for page in doc)
    print(text[:2500])
    print("---TAIL---")
    print(text[-1500:])
    print()
