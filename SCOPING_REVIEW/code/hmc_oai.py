"""Harvest every Human-Machine Communication record from the journal OAI feed.

This is the journal hand search. It collects the table of contents.
It does not decide inclusion.
"""

import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "hmc"
OUT.mkdir(parents=True, exist_ok=True)

NS = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def text(node, path):
    values = node.findall(path, NS)
    return " | ".join((item.text or "").strip() for item in values if (item.text or "").strip())


def main():
    url = (
        "https://stars.library.ucf.edu/do/oai/?verb=ListRecords"
        "&metadataPrefix=oai_dc&set=publication:hmc"
    )
    records = []
    pages = 0
    while url:
        raw = fetch(url)
        pages += 1
        root = ET.fromstring(raw)
        for record in root.findall(".//oai:record", NS):
            header = record.find("oai:header", NS)
            status = header.attrib.get("status") if header is not None else ""
            identifier = text(header, "oai:identifier") if header is not None else ""
            metadata = record.find("oai:metadata", NS)
            dc = metadata.find("oai_dc:dc", NS) if metadata is not None else None
            if dc is None:
                records.append(
                    {
                        "oai_id": identifier,
                        "status": status,
                        "title": "",
                        "creators": "",
                        "date": "",
                        "description": "",
                        "identifier": "",
                        "type": "",
                        "subject": "",
                    }
                )
                continue
            records.append(
                {
                    "oai_id": identifier,
                    "status": status,
                    "title": text(dc, "dc:title"),
                    "creators": text(dc, "dc:creator"),
                    "date": text(dc, "dc:date"),
                    "description": text(dc, "dc:description"),
                    "identifier": text(dc, "dc:identifier"),
                    "type": text(dc, "dc:type"),
                    "subject": text(dc, "dc:subject"),
                }
            )
        token = root.find(".//oai:resumptionToken", NS)
        token_text = (token.text or "").strip() if token is not None else ""
        if token_text:
            url = (
                "https://stars.library.ucf.edu/do/oai/?verb=ListRecords&resumptionToken="
                + urllib.parse.quote(token_text)
            )
            time.sleep(0.5)
        else:
            url = None
        print(f"page {pages}: {len(records)} records", flush=True)
    import json

    (OUT / "hmc_oai_records.json").write_text(
        json.dumps(
            {"harvest_date": "2026-09-29", "records": len(records), "items": records},
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print("saved", len(records))


if __name__ == "__main__":
    main()
