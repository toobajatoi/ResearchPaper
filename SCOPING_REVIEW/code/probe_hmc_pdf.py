"""Try one open-access HMC PDF with a browser user agent."""

import urllib.request
from pathlib import Path

URL = "https://stars.library.ucf.edu/context/hmc/article/1090/viewcontent/06_HMC_VOL6_2023_Concannon_et_al.pdf"
OUT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts"
OUT.mkdir(parents=True, exist_ok=True)
req = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/pdf,*/*",
    },
)
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read(20)
        print("status", resp.status, "start", body[:8])
except Exception as exc:
    print(type(exc).__name__, exc)
