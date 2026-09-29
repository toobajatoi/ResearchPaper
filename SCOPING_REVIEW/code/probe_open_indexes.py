"""One polite probe of OpenAlex and the ACL Anthology metadata file size."""

import json
import urllib.request

URLS = [
    "https://api.openalex.org/works?filter=from_publication_date:2020-01-01,to_publication_date:2026-09-29,title_and_abstract.search:anthropomorphism%20chatbot&per-page=1",
    "https://aclanthology.org/anthology+abstracts.bib.gz",
]


def main():
    for url in URLS:
        req = urllib.request.Request(url, method="GET" if "openalex" in url else "HEAD", headers={"User-Agent": "HMC-scoping-review"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if "openalex" in url:
                    data = json.load(resp)
                    print("openalex", data.get("meta", {}).get("count"), flush=True)
                else:
                    print("acl", resp.status, resp.headers.get("Content-Length"), flush=True)
        except Exception as exc:
            print("FAIL", url[:60], type(exc).__name__, exc, flush=True)


if __name__ == "__main__":
    main()
