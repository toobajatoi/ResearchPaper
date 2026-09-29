"""Search the public ACM and IEEE websites. Save citation metadata, not full texts."""

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publisher_search"
OUT.mkdir(parents=True, exist_ok=True)

QUERY = (
    '("anthropomorphism" OR "anthropomorphic") AND '
    '("large language model" OR "LLM" OR "generative AI")'
)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"


def get(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            return resp.status, resp.geturl(), body
    except urllib.error.HTTPError as exc:
        return exc.code, url, exc.read()


def ieee():
    url = "https://ieeexplore.ieee.org/rest/search"
    payload = {
        "newsearch": True,
        "queryText": QUERY,
        "highlight": False,
        "returnType": "SEARCH",
        "matchPubs": True,
        "ranges": ["2020_2026_Year"],
        "rowsPerPage": 100,
        "pageNumber": 1,
    }
    raw = json.dumps(payload).encode("utf-8")
    status, final, body = get(
        url,
        data=raw,
        headers={
            "User-Agent": UA,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://ieeexplore.ieee.org",
            "Referer": "https://ieeexplore.ieee.org/search/searchresult.jsp",
        },
    )
    path = OUT / "ieee_page1.json"
    path.write_bytes(body)
    note = {"status": status, "url": final, "bytes": len(body)}
    if status == 200:
        try:
            data = json.loads(body.decode("utf-8", errors="replace"))
            note["total"] = data.get("totalRecords")
            note["returned"] = len(data.get("records") or [])
        except json.JSONDecodeError:
            note["parse"] = "not json"
    (OUT / "ieee_note.json").write_text(json.dumps(note, indent=2), encoding="utf-8")
    print("ieee", note, flush=True)


def acm():
    params = urllib.parse.urlencode(
        {
            "fillQuickSearch": "false",
            "target": "advanced",
            "expand": "dl",
            "field1": "AllField",
            "text1": QUERY,
            "AfterYear": "2020",
            "BeforeYear": "2026",
            "pageSize": "20",
            "startPage": "0",
        }
    )
    url = "https://dl.acm.org/action/doSearch?" + params
    status, final, body = get(url, headers={"User-Agent": UA, "Accept": "text/html"})
    path = OUT / "acm_page1.html"
    path.write_bytes(body)
    text = body.decode("utf-8", errors="replace")
    note = {
        "status": status,
        "url": final,
        "bytes": len(body),
        "looks_like_challenge": "Client Challenge" in text or "Just a moment" in text,
        "has_result": "result__count" in text or "items-results" in text,
    }
    (OUT / "acm_note.json").write_text(json.dumps(note, indent=2), encoding="utf-8")
    print("acm", note, flush=True)


if __name__ == "__main__":
    ieee()
    acm()
