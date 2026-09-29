import fitz
from pathlib import Path

doc = fitz.open(Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts" / "queue_user_blocked" / "xie.pdf")
text = "\n".join(page.get_text() for page in doc)
print(text[7000:12000])
