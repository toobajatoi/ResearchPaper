"""Strip arXiv HTML to readable section briefs."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "fulltext" / "arxiv"
OUT = ROOT / "data" / "fulltext" / "arxiv"


def text_of(html):
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    html = re.sub(r"(?i)<h[1-3][^>]*>", "\n## ", html)
    html = re.sub(r"(?i)</h[1-3]>", "\n", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?i)</p>", "\n", html)
    html = re.sub(r"(?is)<[^>]+>", " ", html)
    html = re.sub(r"&nbsp;", " ", html)
    html = re.sub(r"&amp;", "&", html)
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n\s+", "\n", html)
    return html


def main():
    for path in sorted(SRC.glob("*.html")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        text = text_of(raw)
        dest = path.with_suffix(".txt")
        dest.write_text(text, encoding="utf-8")
        print(path.name, len(text), flush=True)


if __name__ == "__main__":
    main()
