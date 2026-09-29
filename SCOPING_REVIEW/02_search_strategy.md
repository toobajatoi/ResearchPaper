# Search strategy

**Status:** Revised 29 September 2026. Scopus and Web of Science are dropped because this review has no subscription. OpenAlex is the multidisciplinary index. ACM Digital Library and IEEE Xplore are searched on their public websites. PubMed, the CASA extra query, the ACL Anthology metadata filter, and the *Human-Machine Communication* hand search have been run. The runs are in `search_execution_log.md`.

**Date of this document:** 29 September 2026.

**Final search date:** Not assigned. The search has not been run. Each database will be dated on the day it is searched. If the databases are searched on different days, every date will be kept. The manuscript will report the date of the last search as the end of the period. No date will be filled in before then.

This strategy implements the eligibility rules in `01_protocol.md`. It is not approval to screen.

## 1. Purpose of the search

The search has to find research that conceptualizes, operationalizes, or measures anthropomorphic communication cues in the text of large language models and closely related generative language systems. It also has to give non-English and cross-lingual research a real chance of being retrieved. A search built only from the English word "anthropomorphism" plus "LLM" would stack the deck toward the claim in the title. That claim is something the review has to test.

Two searches are therefore planned:

- **Search 1, primary.** Anthropomorphism concepts AND generative language systems.
- **Search 2, sensitivity.** Named languages or cross-lingual terms AND generative language systems AND either anthropomorphism concepts or linguistic features that can mark human-like communication even when the paper never says "anthropomorphism."

Search 2 is screened with the same eligibility rules as Search 1. A paper on translation quality, toxicity, or bias is not included just because it is multilingual.

## 2. Concept blocks

Terms inside a block are combined with OR. Blocks are combined with AND. Truncation is marked with `*`. Phrases are in quotes. Exact field syntax for each database is in section 5.

### Block A — anthropomorphic communication

```
anthropomorph*
"human-like" OR "human like" OR humanlike OR "human-likeness" OR "human likeness"
"social cue*" OR "social cues"
"social presence"
"computers are social actors"
"human-machine communication" OR "human machine communication"
```

`CASA` is not used as a bare acronym in the primary string. It matches unrelated names and abbreviations. The phrase "computers are social actors" is used instead. A short extra query, recorded separately, will be:

```
CASA AND (anthropomorph* OR chatbot* OR "language model*" OR LLM OR LLMs)
```

Hits from that extra query will be screened. They will be counted in the identification total only for the databases where the query is actually run.

### Block B — language-generating systems

```
"large language model*" OR "language model*" OR LLM OR LLMs
"generative AI" OR "generative artificial intelligence" OR "generative model*"
chatbot* OR "conversational AI" OR "conversational agent*" OR "dialogue system*" OR "dialog system*"
"AI assistant*" OR "artificial intelligence assistant*" OR "conversational assistant*"
"machine-generated" OR "machine generated" OR "AI-generated" OR "text generation" OR "language technolog*"
```

`LLM` as a bare token will retrieve some irrelevant acronyms. Those are removed at screening. Dropping the bare token would also drop papers that never spell out "large language model."

### Block C — languages and cross-lingual context

Used in Search 2 only. Not required for inclusion.

```
Urdu OR Hindi OR Arabic OR Persian OR Farsi OR Punjabi OR Bengali OR Bangla
Chinese OR Mandarin OR Cantonese OR Japanese OR Korean
Spanish OR French
multilingual OR "cross-lingual" OR crosslingual OR "cross-linguistic" OR crosslinguistic
"non-English" OR "low-resource" OR "South Asian" OR "Global South"
"cultural context*" OR "linguistic variation" OR "linguistic difference*"
```

### Block D — linguistic features

Used in Search 2 only, as an alternative to Block A. These terms retrieve papers that may discuss grammar-dependent or culture-dependent human-like language without using "anthropomorphism."

```
honorific* OR "grammatical gender" OR "address form*" OR "kinship term*"
politeness OR "speech act*" OR "person reference" OR "self-reference" OR "first person" OR "first-person"
pronoun*
```

`pronoun*` is the noisiest term in Block D. If the Search 2 pilot is too large to screen, the first cut will be to require `pronoun*` to sit near a social or anthropomorphic term, and to report that change as a deviation. The cut will not be made silently, and it will not be made before you see the pilot count.

## 3. How the blocks combine

**Search 1**

`(Block A) AND (Block B)`

Date limit: publication year 2020 through the search date. No language limit. No study-design limit.

**Search 2**

`(Block C) AND (Block B) AND (Block A OR Block D)`

Same date limit. No language limit.

Search 2 is a separate result set. Overlap with Search 1 is removed at deduplication, not by dropping Search 2.

## 4. Sources

### 4.0 Change made on 29 September 2026

Scopus and Web of Science are not available without a subscription. They are removed from the source list. The manuscript will not name them as databases that were searched.

OpenAlex replaces them as the multidisciplinary index. It is free and broader than a publisher index, and it is not Scopus or Web of Science. The first OpenAlex Search 1, which copied the wide Block A and Block B string, returned 11,245 title-and-abstract records. A recount the same day that dropped chatbot terms but kept "human-like" and "social presence" still returned 7,330. The query used for export therefore keeps the title-and-abstract field and requires both of the following:

- an anthropomorphism stem: anthropomorphism, anthropomorphic, anthropomorphised, or anthropomorphized;
- an LLM or generative-AI term: "large language model", "large language models", LLM, LLMs, "generative AI", or "generative artificial intelligence".

That query returned 1,411 records. It is the OpenAlex identification set. The wider strings are kept in this file so the deviation is visible. "Human-like" and "social presence" are not silently discarded everywhere: they remain in the PubMed and ACL searches.

IEEE Xplore is a primary source, searched on the public website. Downloading a paywalled PDF is a separate step from searching.

### 4.1 Primary sources

| Source | Role | Interface |
| --- | --- | --- |
| OpenAlex | Multidisciplinary index in place of Scopus and Web of Science | API filter `title_and_abstract.search`, date 2020-01-01 to the search date |
| ACM Digital Library | Computing and HCI, including CHI | Public website search. Title, abstract, and keyword fields where the form allows them. |
| IEEE Xplore | Computing venues not fully covered by ACM | Public website search |
| ACL Anthology | Computational linguistics | Local filter of the public metadata export |
| *Human-Machine Communication* | Target journal | Issue-by-issue hand search at https://stars.library.ucf.edu/hmc/ |

The hand search still happens, because keyword queries miss relevant articles in a small journal. Every research article in each issue from Volume 1 (2020) through the latest issue on the search date is screened. Editorials and news items are logged and excluded with a reason.

### 4.2 Sources not searched

- Scopus.
- Web of Science.
- Communication & Mass Media Complete.
- PsycINFO.

### 4.4 Supplementary sources

Run only after the primary searches are exported and deduplicated.

| Source | Use | What will not be done |
| --- | --- | --- |
| Citation chasing | Backward references and forward citations of every included study, plus the seed records in section 8. One cycle. A second cycle only if the first cycle adds included studies. Stop when a cycle adds none. Tool and date recorded. Scopus cited-by where available; OpenAlex or Semantic Scholar where it is not. | Citation chasing is reported in its own PRISMA box, separate from database hits. |
| PubMed | Narrow Search 1, in case health-communication papers are indexed there and missed elsewhere. | PubMed is not a primary source for this question. |
| Google Scholar | Locate a known seed that the primary indexes missed, and check forward citations when Scopus cited-by is incomplete. | The Google Scholar hit count is not a PRISMA identification total. The result list is not stable or fully exportable. |
| Crossref | Resolve DOIs during charting. | Not a search database for identification. |

OpenAlex is a primary source under section 4.0. Semantic Scholar may still be used for citation chasing when OpenAlex does not return a citing list. Neither one is a substitute for a database that was not searched.

## 5. Database strings

These strings have not been run. The first action after approval is a Scopus pilot of Search 1 and Search 2. You will see the hit counts before any full export or screening. If a count is unmanageable, the string will be tightened only with your approval, and both versions will be kept in the record.

Placeholders written as `SEARCH_DATE` are not dates. They are replaced with the real calendar date on the day of the search.

Field choice for the primary search is title, abstract, and keywords. Full text is not the primary field. Full-text search would inflate the set with passing mentions.

### 5.1 Scopus

Search 1:

```
TITLE-ABS-KEY(
  (anthropomorph* OR "human-like" OR "human like" OR humanlike OR "human-likeness" OR "human likeness" OR "social cue*" OR "social presence" OR "computers are social actors" OR "human-machine communication" OR "human machine communication")
  AND
  ("large language model*" OR "language model*" OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR "generative model*" OR chatbot* OR "conversational AI" OR "conversational agent*" OR "dialogue system*" OR "dialog system*" OR "AI assistant*" OR "artificial intelligence assistant*" OR "conversational assistant*" OR "machine-generated" OR "machine generated" OR "AI-generated" OR "text generation" OR "language technolog*")
)
AND PUBYEAR > 2019
AND PUBYEAR < SEARCH_YEAR_PLUS_ONE
```

`SEARCH_YEAR_PLUS_ONE` is the year after the search year, so a search in 2026 uses `PUBYEAR < 2027`. The day within the final year is recorded from the search session, because Scopus year limits do not store the day.

Do not add a `LANGUAGE()` limit.

Search 2 uses the same system block and the same year limits, with this concept block in place of Block A alone:

```
(
  (Urdu OR Hindi OR Arabic OR Persian OR Farsi OR Punjabi OR Bengali OR Bangla OR Chinese OR Mandarin OR Cantonese OR Japanese OR Korean OR Spanish OR French OR multilingual OR "cross-lingual" OR crosslingual OR "cross-linguistic" OR crosslinguistic OR "non-English" OR "low-resource" OR "South Asian" OR "Global South" OR "cultural context*" OR "linguistic variation" OR "linguistic difference*")
  AND
  (anthropomorph* OR "human-like" OR "human like" OR humanlike OR "human-likeness" OR "human likeness" OR "social cue*" OR "social presence" OR "computers are social actors" OR "human-machine communication" OR "human machine communication" OR honorific* OR "grammatical gender" OR "address form*" OR "kinship term*" OR politeness OR "speech act*" OR "person reference" OR "self-reference" OR "first person" OR "first-person" OR pronoun*)
)
```

The CASA extra query:

```
TITLE-ABS-KEY(CASA AND (anthropomorph* OR chatbot* OR "language model*" OR LLM OR LLMs))
AND PUBYEAR > 2019 AND PUBYEAR < SEARCH_YEAR_PLUS_ONE
```

Export: full record with abstract, author keywords, DOI, and document type. Save the Scopus search history printout or the query text and the hit count on the day.

### 5.2 Web of Science

Core collection topic search. Indexes actually queried will be copied from the results page.

Search 1:

```
TS=(
  (anthropomorph* OR "human-like" OR "human like" OR humanlike OR "human-likeness" OR "human likeness" OR "social cue*" OR "social presence" OR "computers are social actors" OR "human-machine communication" OR "human machine communication")
  AND
  ("large language model*" OR "language model*" OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR "generative model*" OR chatbot* OR "conversational AI" OR "conversational agent*" OR "dialogue system*" OR "dialog system*" OR "AI assistant*" OR "artificial intelligence assistant*" OR "conversational assistant*" OR "machine-generated" OR "machine generated" OR "AI-generated" OR "text generation" OR "language technolog*")
)
```

Timespan: `2020-01-01` to `SEARCH_DATE`. No language limit.

Search 2: same system block, timespan, and the Block C AND (Block A OR Block D) structure from section 3. The CASA extra query is run with the same timespan.

Export: full record and cited references if the subscription allows. Save the query and the hit count.

### 5.3 ACM Digital Library

Search the **ACM Guide to Computing Literature**. Use Advanced Search, then Edit Query, so title, abstract, and keyword can be combined with OR. The default line combination is AND, which would force a term to occur in every field. That is the wrong interpretation of this strategy.

Date filter: custom range 1 January 2020 through `SEARCH_DATE`.

Search 1, draft for the Edit Query box:

```
(Title:(anthropomorph* OR "human-like" OR "human like" OR humanlike OR "human-likeness" OR "human likeness" OR "social cue*" OR "social presence" OR "computers are social actors" OR "human-machine communication" OR "human machine communication")
OR Abstract:(anthropomorph* OR "human-like" OR "human like" OR humanlike OR "human-likeness" OR "human likeness" OR "social cue*" OR "social presence" OR "computers are social actors" OR "human-machine communication" OR "human machine communication")
OR Keyword:(anthropomorph* OR "human-like" OR "human like" OR humanlike OR "human-likeness" OR "human likeness" OR "social cue*" OR "social presence" OR "computers are social actors" OR "human-machine communication" OR "human machine communication"))
AND
(Title:("large language model*" OR "language model*" OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR "generative model*" OR chatbot* OR "conversational AI" OR "conversational agent*" OR "dialogue system*" OR "dialog system*" OR "AI assistant*" OR "artificial intelligence assistant*" OR "conversational assistant*" OR "machine-generated" OR "machine generated" OR "AI-generated" OR "text generation" OR "language technolog*")
OR Abstract:("large language model*" OR "language model*" OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR "generative model*" OR chatbot* OR "conversational AI" OR "conversational agent*" OR "dialogue system*" OR "dialog system*" OR "AI assistant*" OR "artificial intelligence assistant*" OR "conversational assistant*" OR "machine-generated" OR "machine generated" OR "AI-generated" OR "text generation" OR "language technolog*")
OR Keyword:("large language model*" OR "language model*" OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR "generative model*" OR chatbot* OR "conversational AI" OR "conversational agent*" OR "dialogue system*" OR "dialog system*" OR "AI assistant*" OR "artificial intelligence assistant*" OR "conversational assistant*" OR "machine-generated" OR "machine generated" OR "AI-generated" OR "text generation" OR "language technolog*"))
```

ACM's exported query syntax is the version of record for the search, not this draft. On the day, export the syntax CSV (syntax, date, hit count) and store it. If the interface rejects the draft, the working query is the exported one, and the difference will be written down.

Search 2 is the same field pattern with Block C AND (Block A OR Block D). It may need to be split into two ACM queries if the interface truncates the string. Splits will be documented. Their union is the Search 2 set for ACM.

### 5.4 ACL Anthology

The Anthology website search is not a stable Boolean system equivalent to Scopus. The reproducible search is a local filter of the official public metadata export.

On the search date:

1. Download the public Anthology metadata (the bibliography or JSON export maintained with https://github.com/acl-org/acl-anthology). Record the file name, download URL, date, and a file hash.
2. Keep records whose publication year is 2020 through the search year.
3. Apply Search 1 and Search 2 to title and abstract only.
4. Run a simplified keyword search on https://aclanthology.org/ as a check. Reconcile anything the website returns that the metadata filter missed, and the reverse.
5. Save the filter script and the hit list. The script will be written only after you approve this strategy. It will not call any model API.

### 5.5 Human-Machine Communication hand search

Source: https://stars.library.ucf.edu/hmc/

For each volume and issue available on the search date, record the volume, issue, article title, and decision (retained for abstract/full-text screening, or excluded at title with a reason). This is a census of the journal's research articles in the period, not a keyword search inside the journal.

### 5.6 IEEE Xplore, if approved

Command Search draft, to be confirmed against the interface on the day. The saved search string from IEEE is the version of record.

Search 1:

```
("Document Title":anthropomorph* OR "Abstract":anthropomorph* OR "Author Keywords":anthropomorph* OR "Document Title":"human-like" OR "Abstract":"human-like" OR "Document Title":"social presence" OR "Abstract":"social presence" OR "Document Title":"computers are social actors" OR "Abstract":"computers are social actors" OR "Document Title":"human-machine communication" OR "Abstract":"human-machine communication")
AND
("Document Title":"large language model" OR "Abstract":"large language model" OR "Document Title":"language model" OR "Abstract":"language model" OR "Document Title":LLM OR "Abstract":LLM OR "Document Title":chatbot OR "Abstract":chatbot OR "Document Title":"conversational agent" OR "Abstract":"conversational agent" OR "Document Title":"generative AI" OR "Abstract":"generative AI")
```

Year: 2020 through `SEARCH_DATE`. The IEEE draft is slightly narrower than Scopus because the command-search field syntax is verbose. If you approve IEEE, the pilot will check whether this narrower string is acceptable or whether it should be expanded toward the Scopus term list. Expansion happens before the full export, and only with the difference recorded.

### 5.7 PubMed supplementary

```
(anthropomorph*[tiab] OR "human-like"[tiab] OR "human likeness"[tiab] OR "social presence"[tiab] OR "social cue*"[tiab] OR "computers are social actors"[tiab] OR "human-machine communication"[tiab])
AND
("large language model*"[tiab] OR "language model*"[tiab] OR chatbot*[tiab] OR "generative AI"[tiab] OR "generative artificial intelligence"[tiab] OR "conversational agent*"[tiab] OR "conversational AI"[tiab])
AND
("2020/01/01"[Date - Publication] : "SEARCH_DATE"[Date - Publication])
```

No language limit. This is Search 1 only. A PubMed Search 2 will be added only if the primary Search 2 shows that health journals are an important missing source. That decision will be recorded.

## 6. Limits that will and will not be used

| Limit | Decision |
| --- | --- |
| Date | 1 January 2020 through the search date |
| Publication language | No limit |
| Species, age, or human-subject filters | Not used |
| Full text available online | Not used as a search limit. Inaccessibility is an exclusion reason at full text, after an attempt to retrieve the paper |
| Document type | Not limited in the database. Editorials, news, and blogs are excluded at screening |

## 7. Deduplication and the PRISMA counts

After export:

1. Exact DOI match.
2. Normalized title plus year, for records with no DOI.
3. Manual check of probable duplicates before any are removed.

Counts that will be stored, and only after they exist:

- identified, by source, for Search 1 and Search 2 separately and combined;
- duplicates removed;
- title and abstract screened;
- excluded at title and abstract;
- full texts sought and full texts not retrieved;
- full texts assessed;
- excluded at full text, with one reason each;
- included.

The PRISMA flow diagram will be drawn from that log. It will not be drawn from estimates. `data/screening.csv` and `05_screening_log.csv` will be created when the exports exist.

Full-text exclusion reasons will use a closed list, expanded only when a real paper does not fit:

- not a language-generating system of the included type;
- no anthropomorphic or human-like communication construct;
- no analysis or conceptualization of textual or linguistic cues;
- robot, voice, or visual anthropomorphism only;
- not a scholarly source;
- duplicate;
- full text not available;
- not enough information to chart.

## 8. Seed records for citation chasing

Located on 29 September 2026. Not yet included. Full texts have not been charted.

- DeVrio, A., Cheng, M., Egede, L., Olteanu, A., & Blodgett, S. L. (2025). A taxonomy of linguistic expressions that contribute to anthropomorphism of language technologies. CHI 2025. https://doi.org/10.1145/3706598.3714038
- Ibrahim, L., Akbulut, C., Elasmar, R., Rastogi, C., Kahng, M., Morris, M., McKee, K., Rieser, V., Shanahan, M., & Weidinger, L. (2026). Multi-turn evaluation of anthropomorphic behaviours in large language models. ICLR 2026. https://proceedings.iclr.cc/paper_files/paper/2026/hash/fccb2556dbe783422a27f2b71e5c47da-Abstract-Conference.html and preprint https://arxiv.org/abs/2502.07077
- ACL 2025 paper *Dehumanizing machines: Mitigating anthropomorphic behaviors in text generation systems*, https://aclanthology.org/2025.acl-long.1259/, https://doi.org/10.18653/v1/2025.acl-long.1259. Authors will be copied from the Anthology record when the paper is retrieved.

These seeds are also a check on the strings. After the first Scopus pilot, the strategy should be able to retrieve the DeVrio and Ibrahim records from at least one primary source. If it cannot, the string will be revised before the full search, and you will be told why.

## 9. What this document does not do

- It does not report hit counts.
- It does not set the final search date.
- It does not start screening.
- It does not treat the three-way cue framework as a search result.
