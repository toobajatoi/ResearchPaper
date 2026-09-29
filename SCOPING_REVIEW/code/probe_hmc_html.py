import re
import urllib.request

url = "https://stars.library.ucf.edu/hmc/vol13/iss1/2"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=40) as resp:
    html = resp.read().decode("utf-8", "replace")
print("bytes", len(html))
for match in re.findall(r'href="([^"]+)"', html):
    if "pdf" in match.lower() or "download" in match.lower():
        print(match[:180])
idx = html.lower().find("abstract")
print("---")
print(re.sub(r"\s+", " ", html[idx : idx + 800]) if idx >= 0 else "no abstract")
