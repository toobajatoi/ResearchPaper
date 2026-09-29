"""Add language_evident_from_examples. Does not rebuild the matrix."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "evidence_matrix.csv"
OUT_TABLE = ROOT / "data" / "fulltext" / "oa_attempts" / "table2.md"

# Language of the examples, prompts, or dataset, only where the text read shows it.
# Keys are study_id. Values are short labels.
EVIDENT = {
    # Authors state the language of the communication, cases, data, or examples.
    "PMID:42792503": "English",
    "PMID:42528981": "English",
    "PMID:42487918": "English",
    "PMID:41234618": "Korean",
    "PMID:38957452": "English",
    "PMID:37938776": "English",
    "PMID:42507678": "Japanese",
    "https://doi.org/10.1145/3706598.3714038": "English",
    "https://arxiv.org/abs/2502.07077": "English",
    "https://aclanthology.org/2023.emnlp-main.290/": "English",
    "https://aclanthology.org/2026.findings-eacl.4/": "English",
    "https://aclanthology.org/2026.acl-long.241/": "English and Japanese",
    "https://aclanthology.org/2025.acl-long.1261/": "English",
    "https://aclanthology.org/2024.lrec-main.1166/": "Korean",
    "https://doi.org/10.48550/arxiv.2409.15769": "English",
    "https://doi.org/10.48550/arxiv.2605.07925": "English",
    "https://doi.org/10.1145/3715275.3732045": "Standard American English, African American English, and Queer slang",
    "https://doi.org/10.48448/cp8f-z717": "Chinese",
    "https://doi.org/10.5281/zenodo.17724016": "Dutch and English",
    "https://doi.org/10.1515/lass-2026-0021": "English",
    "https://doi.org/10.1109/access.2026.3707234": "Korean",
    # Not stated, but examples, prompts, or dataset excerpts in the text read are English.
    "https://aclanthology.org/2025.coling-main.239/": "English",
    "https://aclanthology.org/2026.clpsych-1.26/": "English",
    "https://aclanthology.org/2024.sigdial-1.21/": "English",
    "https://arxiv.org/abs/2508.09998": "English",
    "https://doi.org/10.1145/3771844": "English",
    "https://doi.org/10.48550/arxiv.2605.28305": "English",
    "https://doi.org/10.48550/arxiv.2606.02493": "English",
    "https://doi.org/10.1145/3786304.3787880": "English",
    "https://doi.org/10.5281/zenodo.19544710": "English",
    "https://doi.org/10.5281/zenodo.22871049": "English",
    "https://aclanthology.org/2024.findings-emnlp.567/": "English",
    "https://doi.org/10.48550/arxiv.2409.02244": "English",
    "https://doi.org/10.48550/arxiv.2601.08874": "English",
    "https://doi.org/10.1145/3630106.3658956": "English",
}

# Reviews that restrict the publication language. That is not the language of model examples.
PUBLICATION_ONLY = {
    "PMID:39661968",
    "https://doi.org/10.48550/arxiv.2607.18250",
}

SHORT = {
    "PMID:42792503": "Liu et al. (2026)",
    "PMID:42721382": "Maurich Novelli et al. (2026)",
    "PMID:42712761": "Shih (2026)",
    "PMID:42528981": "Li et al. (2026)",
    "PMID:42487918": "Silacci et al. (2026)",
    "PMID:41234618": "Kim et al. (2025), BetterMood",
    "PMID:41060458": "Monteith et al. (2026)",
    "PMID:40378006": "Peter et al. (2025)",
    "PMID:38958218": "Ferrario et al. (2024)",
    "PMID:38957452": "Liu (2024)",
    "PMID:39661968": "Sorin et al. (2024)",
    "PMID:40123640": "Reinecke et al. (2025)",
    "PMID:37938776": "Shanahan et al. (2023)",
    "PMID:42507678": "Gao et al. (2026)",
    "https://doi.org/10.1145/3706598.3714038": "DeVrio et al. (2025)",
    "https://arxiv.org/abs/2502.07077": "Ibrahim et al. (2026)",
    "https://doi.org/10.18653/v1/2025.acl-long.1259": "Cheng et al. (2025)",
    "https://aclanthology.org/2025.sicon-1.10/": "Kim et al. (2025), OverlapBot",
    "https://aclanthology.org/2025.emnlp-main.164/": "Xiao et al. (2025)",
    "https://aclanthology.org/2025.coling-main.239/": "Song et al. (2025)",
    "https://aclanthology.org/2024.findings-emnlp.567/": "Li et al. (2024)",
    "https://aclanthology.org/2023.ranlp-1.18/": "Belkhir and Sadat (2023)",
    "https://aclanthology.org/2023.emnlp-main.290/": "Abercrombie et al. (2023)",
    "https://aclanthology.org/2026.findings-eacl.4/": "Affective hallucination (2026)",
    "https://aclanthology.org/2026.clpsych-1.26/": "Attachment Index (2026)",
    "https://aclanthology.org/2026.acl-long.241/": "Backchannels (2026)",
    "https://aclanthology.org/2025.findings-acl.328/": "P-React (2025)",
    "https://aclanthology.org/2025.acl-long.1261/": "HumT (2025)",
    "https://aclanthology.org/2024.sigdial-1.21/": "Self-emotion (2024)",
    "https://aclanthology.org/2024.lrec-main.1166/": "PSYDIAL (2024)",
    "https://doi.org/10.48550/arxiv.2503.10728": "DarkBench (2025)",
    "https://doi.org/10.48550/arxiv.2405.13803": "Wu et al. (2024), Sunnie",
    "https://doi.org/10.48550/arxiv.2409.02244": "Iftikhar et al. (2024)",
    "https://doi.org/10.48550/arxiv.2409.15769": "Li et al. (2024), in situ",
    "https://doi.org/10.1145/3771844": "Krämer et al. (2025)",
    "https://doi.org/10.48550/arxiv.2605.28305": "Yu et al. (2026)",
    "https://doi.org/10.48550/arxiv.2607.18250": "Jayathilake and Ma (2026)",
    "https://doi.org/10.48550/arxiv.2606.02493": "Pawar et al. (2026)",
    "https://doi.org/10.48550/arxiv.2603.19030": "Zierahn et al. (2026)",
    "https://doi.org/10.48550/arxiv.2605.07925": "Arora et al. (2026)",
    "https://doi.org/10.48550/arxiv.2606.08172": "Reani et al. (2026)",
    "https://doi.org/10.48550/arxiv.2407.11977": "Sun et al. (2024)",
    "https://doi.org/10.48550/arxiv.2605.23787": "Vecchione et al. (2026)",
    "https://doi.org/10.48550/arxiv.2601.08874": "Islam (2026)",
    "https://arxiv.org/abs/2508.09998": "INTIMA (2026)",
    "https://doi.org/10.1145/3630106.3658956": "Maeda (2024), parasocial",
    "https://doi.org/10.1609/aies.v7i1.31613": "Akbulut (2024)",
    "https://doi.org/10.1145/3715275.3732045": "Basoah et al. (2025)",
    "https://doi.org/10.1145/3805689.3812324": "Ferrario (2026), ethics review",
    "https://doi.org/10.2139/ssrn.5404666": "Nath (2025)",
    "https://doi.org/10.1609/aies.v7i2.31903": "Maeda (2025), capabilities",
    "https://doi.org/10.1016/j.chbah.2026.100296": "Azeem (2026)",
    "https://doi.org/10.1007/s10676-026-09917-x": "Labuz (2026)",
    "https://doi.org/10.5281/zenodo.18062879": "Hudson (2025)",
    "https://doi.org/10.5281/zenodo.17943125": "Walton (2025)",
    "https://doi.org/10.2196/preprints.99710": "Keskin (2026)",
    "https://doi.org/10.29038/eejpl.2026.13.1.mug": "Mugableh (2026)",
    "https://doi.org/10.2139/ssrn.5813342": "Phillips (2026)",
    "https://doi.org/10.48448/cp8f-z717": "Fan and Liu (2025)",
    "https://doi.org/10.5281/zenodo.19565195": "Rowland (2026)",
    "https://doi.org/10.1145/3786304.3787880": "Ayad (2026)",
    "https://doi.org/10.31235/osf.io/u3qc9_v1": "Prestes (2025)",
    "https://doi.org/10.5281/zenodo.17724016": "EMA casebook (2025)",
    "https://doi.org/10.2139/ssrn.5431338": "Zhang (2025)",
    "https://doi.org/10.1515/lass-2026-0021": "Alkhayat (2026)",
    "https://doi.org/10.5281/zenodo.21056974": "Hrubec (2026)",
    "https://doi.org/10.1109/access.2026.3707234": "OSED-Ko (2026)",
    "https://doi.org/10.5281/zenodo.19544710": "Spisländer (2026)",
    "https://doi.org/10.5281/zenodo.22871049": "Ngwu (2026)",
}


def stated_label(raw):
    text = (raw or "").strip()
    if not text or text.lower().startswith("not stated"):
        return "Not stated"
    return text


def clip(text, n):
    text = " ".join((text or "").replace("|", "/").replace("\n", " ").split())
    if len(text) <= n:
        return text or "Not charted"
    cut = text[:n]
    if "; " in cut:
        cut = cut.rsplit("; ", 1)[0]
    return cut.rstrip(" ,;")


def system_label(raw):
    text = " ".join((raw or "").replace("|", "/").replace("\n", " ").split())
    if not text or text.lower().startswith("not stated"):
        return "Not named"
    return clip(text, 90)


def main():
    rows = list(csv.DictReader(MATRIX.open(encoding="utf-8")))
    fields = list(rows[0].keys())
    if "language_evident_from_examples" not in fields:
        # Place the new column immediately after the stated-language column.
        idx = fields.index("language_of_communication") + 1
        fields.insert(idx, "language_evident_from_examples")
    n_stated = n_evident = n_both_blank = 0
    lines = [
        "| Source | Study type | System | Language stated | Language evident from examples | Cue labels in the source’s terms |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        sid = row["study_id"]
        stated = stated_label(row.get("language_of_communication"))
        if sid in EVIDENT:
            evident = EVIDENT[sid]
        elif sid in PUBLICATION_ONLY:
            evident = "Not evident from model examples"
        else:
            evident = "Not evident in the text read"
        row["language_evident_from_examples"] = evident
        if stated != "Not stated":
            n_stated += 1
        if not evident.startswith("Not evident"):
            n_evident += 1
        if stated == "Not stated" and evident.startswith("Not evident"):
            n_both_blank += 1
        source = SHORT.get(sid, clip(row.get("citation"), 40))
        lines.append(
            "| {src} | {st} | {sys} | {stated} | {ev} | {cue} |".format(
                src=source,
                st=clip(row.get("study_type"), 42),
                sys=system_label(row.get("system_or_llm")),
                stated=stated.replace("|", "/"),
                ev=evident.replace("|", "/"),
                cue=clip(row.get("cue_category_in_source_terms"), 160),
            )
        )
    with MATRIX.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    OUT_TABLE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("rows", len(rows))
    print("stated", n_stated)
    print("evident", n_evident)
    print("neither", n_both_blank)
    print("not stated but evident", n_evident - (n_stated - len(PUBLICATION_ONLY & set(SHORT))))


if __name__ == "__main__":
    main()
