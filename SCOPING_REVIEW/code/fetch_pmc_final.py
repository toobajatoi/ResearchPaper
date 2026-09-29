import json
import urllib.parse
import urllib.request
from pathlib import Path

PMIDS = ["42269974", "41548427", "41438004", "40286349", "42277102"]
OUT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "oa_attempts" / "queue_final"
OUT.mkdir(parents=True, exist_ok=True)
query = " OR ".join(f"EXT_ID:{pmid}" for pmid in PMIDS)
url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(
    {"query": query, "format": "json", "resultType": "core", "pageSize": "10"}
)
request = urllib.request.Request(url, headers={"User-Agent": "research-screening"})
data = json.loads(urllib.request.urlopen(request, timeout=40).read())
for record in data.get("resultList", {}).get("result", []):
    pmid = record.get("pmid")
    pmcid = record.get("pmcid")
    print(pmid, pmcid, record.get("isOpenAccess"), (record.get("title") or "")[:80])
    if not pmcid:
        continue
    pdf_url = f"https://europepmc.org/articles/{pmcid}?pdf=render"
    dest = OUT / f"{pmid}.pdf"
    try:
        pdf_request = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
        blob = urllib.request.urlopen(pdf_request, timeout=60).read()
        dest.write_bytes(blob)
        print(" pdf", len(blob), blob[:8])
    except Exception as error:
        print(" pdf ERR", error)
