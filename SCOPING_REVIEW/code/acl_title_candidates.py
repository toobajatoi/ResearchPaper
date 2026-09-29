"""Split ACL title lists into cue-relevant titles and the rest.

This is a title screen, not an inclusion decision. A title is kept for
abstract reading when it names anthropomorphism or a communicative cue.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "acl"

KEEP = re.compile(
    r"anthropomorph|empath|\bpersonas?\b|politeness|honorific|sycoph|"
    r"social presence|human-likeness|human likeness|address form|kinship|"
    r"first-person|first person|\bpronoun|"
    r"human-like.{0,40}(chat|dialog|dialogue|conversation|agent)|"
    r"(chat|dialog|dialogue|conversation|agent).{0,40}human-like",
    re.I,
)


def main():
    for name in ("search1", "search2"):
        lines = (SRC / f"{name}_titles.txt").read_text(encoding="utf-8").splitlines()
        keep = [line for line in lines if KEEP.search(line)]
        drop = [line for line in lines if line not in keep]
        (SRC / f"{name}_title_keep.txt").write_text("\n".join(keep), encoding="utf-8")
        (SRC / f"{name}_title_exclude.txt").write_text("\n".join(drop), encoding="utf-8")
        print(name, "keep", len(keep), "exclude_title", len(drop), flush=True)


if __name__ == "__main__":
    main()
