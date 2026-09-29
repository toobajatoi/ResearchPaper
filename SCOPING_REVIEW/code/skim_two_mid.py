import fitz
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts" / "queue_user_blocked"

doc = fitz.open(ROOT / "ijfmr_banking.pdf")
text = "\n".join(page.get_text() for page in doc)
# print from methods-ish
idx = text.lower().find("method")
print("BANK idx", idx)
print(text[idx:idx+3500] if idx > 0 else text[4000:7500])
print("\n\n==== XIE MIDDLE ====\n")
doc = fitz.open(ROOT / "xie.pdf")
text = "\n".join(page.get_text() for page in doc)
print(text[2500:7000])
