import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts" / "queue_user_blocked"
OUT.mkdir(parents=True, exist_ok=True)


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read(), response.geturl(), response.headers.get("Content-Type", "")


data, final, ctype = get("https://www.ijfmr.com/papers/2026/3/87300.pdf")
(OUT / "ijfmr_banking.pdf").write_bytes(data)
print("ijfmr", len(data), final, ctype)

html, final, ctype = get("https://chr.ewaoa.com/article/view/16325")
text = html.decode("utf-8", "replace")
print("xie", len(text), final)
for match in re.findall(r'href="([^"]+)"', text):
    if "pdf" in match.lower() or "download" in match.lower():
        print("link", match[:240])
