"""Show ACL Search 1 titles the broader rule would add. Does not change screening."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "acl"
OLD = re.compile(
    r"anthropomorph|empath|\bpersonas?\b|politeness|honorific|sycoph|"
    r"social presence|human-likeness|human likeness|address form|kinship|"
    r"first-person|first person|\bpronoun|"
    r"human-like.{0,40}(chat|dialog|dialogue|conversation|agent)|"
    r"(chat|dialog|dialogue|conversation|agent).{0,40}human-like",
    re.I,
)
NEW = re.compile(
    r"anthropomorph|empath|human-like|humanlike|human likeness|"
    r"affective|emotional language|\bemotions?\b|"
    r"\bpersonas?\b|\bpersonality\b|politeness|honorific|sycoph|"
    r"social presence|role-?play|\bcompanions?(hip)?\b|"
    r"relational|social behavio|backchannel|\bfillers?\b|"
    r"address form|kinship|first-person|first person|\bpronoun",
    re.I,
)

lines = (ROOT / "search1_titles.txt").read_text(encoding="utf-8").splitlines()
added = [line for line in lines if NEW.search(line) and not OLD.search(line)]
print("added", len(added))
(ROOT / "search1_broader_added.txt").write_text("\n".join(added), encoding="utf-8")
