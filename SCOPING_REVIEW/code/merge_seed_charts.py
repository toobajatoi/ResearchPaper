"""Merge the three seed charting rows into the evidence matrix.

The source table is the author-supplied CSV. A few cells are corrected to
match the full text that was checked.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "evidence_matrix.csv"
SOURCE = Path(r"C:\Users\tooba\Downloads\charted_rows_seed_papers.csv")
SAMPLE = ROOT / "data" / "author_verification_sample.csv"

CORRECTIONS = {
    "PMID:37938776": {
        "citation": "Shanahan, M., McDonell, K., & Reynolds, L. (2023). Role play with large language models. Nature, 623, 493-498. https://doi.org/10.1038/s41586-023-06647-8",
        "dataset_or_sample": "None. Illustrative examples only: reported Bing Chat exchanges (February 2023) and one ChatGPT query (4 May 2023).",
        "charting_status": "Author-verified. Charted from arXiv 2305.16367v1 (25 May 2023). Volume 623 and pages 493-498 were confirmed from Crossref. The Nature HTML was not opened.",
    },
    "https://doi.org/10.1145/3706598.3714038": {
        "dataset_or_sample": "50 public sources (news, research, and social media; 2017-2024, 90% from 2022-2024); 395 cases (each one conversational turn); 3954 annotations; purposeful sampling to saturation.",
        "operationalization": "Iterative bottom-up thematic analysis of verbatim outputs in the context of inputs. At least two researchers annotated each output, followed by interpretation sessions. Affinity diagramming grouped expressions from prior taxonomies and compared them with the empirical codes.",
        "charting_status": "Author-verified. Charted from the CHI '25 text. Numbers checked on arXiv 2502.09870, which is the same paper: 50 sources, 395 cases, 3954 annotations.",
    },
    "https://arxiv.org/abs/2502.07077": {
        "url": "https://arxiv.org/abs/2502.07077v3",
        "measurement_method": "Three Judge LLMs (gemini-1.5-flash-002, claude-3-5-sonnet-20240620, gpt-4-turbo-2024-04-09), 3 samples each, mode then majority vote. First-person pronouns counted with a regex. Human raters' Krippendorff's alpha on the 13 judged behaviours is 0.101-0.616 (Table 4). For the majority of behaviours, weighted average precision is over 85%. Kruskal-Wallis and Mann-Whitney tests. Validation via the Godspeed Anthropomorphism survey and AnthroScore.",
        "findings": "All four systems show similar profiles dominated by relationship-building and first-person pronouns. Validation and first-person pronouns are the only two behaviours in over 50% of messages for all four systems. Friendship and life coaching show the most anthropomorphic behaviour. For 9 of 14 behaviours, 50% or more of instances first appear in turns 2-5. An anthropomorphic behaviour in one turn raises the likelihood of anthropomorphic behaviour in later turns. The high-frequency condition was rated more anthropomorphic on the Godspeed average of the four items (4.00 vs 3.25; the text also reports 4 and 3.25; U = 213636, p < .001, r = .411) and more implicitly human-framed on AnthroScore (U = 158699, p < .05).",
        "limitations_stated_by_authors": "English and Western focus. One type of user simulation. Only five turns. Non-adversarial dialogues are not an upper bound. Human agreement is described as spanning poor to moderate. Empathy has the lowest average percent agreement (55.57%).",
        "charting_status": "Author-verified. Charted from arXiv 2502.07077v3 (2 February 2026). The PDF is labelled Published as a conference paper at ICLR 2026. Numbers checked on that PDF: 960 dialogues, N = 1101, Godspeed averages 4.00 and 3.25.",
    },
}

NOTES = {
    "PMID:37938776": "Author-verified. Charted from arXiv 2305.16367v1. The Nature HTML was not opened.",
    "https://doi.org/10.1145/3706598.3714038": "Author-verified. Charted from the CHI '25 text. Numbers checked on arXiv 2502.09870.",
    "https://arxiv.org/abs/2502.07077": "Author-verified. Charted from arXiv 2502.07077v3, the ICLR 2026 camera-ready PDF.",
}


def main():
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        incoming = {row["study_id"]: row for row in csv.DictReader(handle)}
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys())
    hit = 0
    for row in rows:
        study_id = row["study_id"]
        if study_id not in incoming:
            continue
        for key in fields:
            value = incoming[study_id].get(key)
            if value:
                row[key] = value
        row.update(CORRECTIONS[study_id])
        hit += 1
    if hit != 3:
        raise SystemExit("expected 3 merged rows, found %s" % hit)
    with MATRIX.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    with SAMPLE.open(encoding="utf-8", newline="") as handle:
        sample = list(csv.DictReader(handle))
        sample_fields = list(sample[0].keys())
    noted = 0
    for row in sample:
        if row["identifier"] in NOTES:
            row["author_note"] = NOTES[row["identifier"]]
            noted += 1
    with SAMPLE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=sample_fields)
        writer.writeheader()
        writer.writerows(sample)
    print("merged", hit, "notes", noted)


if __name__ == "__main__":
    main()
