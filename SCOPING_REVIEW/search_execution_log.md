# Search execution log

**Search date for the searches below:** 29 September 2026.

This log records what was actually run. It does not replace `02_search_strategy.md`.

## Subscription databases

Scopus, Web of Science, the ACM Digital Library, and IEEE Xplore were not searched. This environment has no subscription login for them. Their absence is a limit of this run, not a decision to drop them from the protocol. They still need to be searched before the review can be called complete.

## OpenAlex

OpenAlex was queried because it is openly accessible. It is an extra source. It is not a substitute for Scopus or Web of Science.

Search 1, title and abstract, 1 January 2020 through 29 September 2026, returned a reported count of **11,243**. The Boolean AND was checked with smaller queries before the full pull:

| Query | Reported count |
| --- | --- |
| anthropomorphism | 6,251 |
| anthropomorphism AND chatbot | 737 |
| "large language model" AND anthropomorphism | 311 |

The full Search 1 export did not finish. About 9,000 records were received and then the service returned HTTP 429. Those pages were not saved, because the first script wrote the file only at the end. A second attempt was stopped after the first page was also rate-limited, so that the service would not be queried again in a loop. No OpenAlex records are in the screening file.

The query text is in `code/openalex_search.py`.

## PubMed

Supplementary Search 1 was run on 29 September 2026. PubMed reported **650** records. The PMIDs are in `data/pubmed/search1_ids.json`. Titles, authors, journals, and dates for all 650 are in `data/pubmed/search1_summaries.json`. Title and abstract screening is recorded below.

## Human-Machine Communication

The journal OAI feed was harvested on 29 September 2026 from https://stars.library.ucf.edu/do/oai/ with set `publication:hmc`. **131** records were saved, including complete-volume files. The raw harvest is `data/hmc/hmc_oai_records.json`.

Title and abstract screening of those 131 records is in `data/screening.csv`.

- Retained for full-text reading: 15
- Excluded at title/abstract: 116

The journal PDF links returned HTTP 403, so those 15 full texts have not been read. One article page was opened (Ischen, Wang, and Smit, 2026, DOI 10.30658/hmc.13.2). Its abstract describes a typology of appearance-based, capacity-based, and personality-based human-likeness for text-based conversational agents, and a test of social cues in customer-service chatbots. That abstract is not an inclusion decision.

## PubMed title and abstract screening

All 650 titles were read. 86 were kept for abstract reading and 564 were excluded at title. Abstracts were fetched for all 86. After the abstracts were read:

- Kept for full-text reading: 57
- Excluded at abstract: 29

These 57 were a full-text queue, not included studies.

The DOI stored with the PubMed abstracts was the last `ArticleId` in each record, which was often a cited reference. PubMed esummary article identifiers replaced those DOIs in `data/fulltext/availability.json` on 29 September 2026. That correction changed 47 of 57 DOIs and added three PMCIDs that the Europe PMC PMID search had missed: PMC7617520, PMC11669866, and PMC11617003.

## PubMed full text

Europe PMC full text was downloaded for 46 of the 57 records. Each XML title was checked against the PubMed title. Full-text decisions are in `data/screening.csv` and `data/fulltext/decisions/final_decisions.json`.

- Included: 21
- Excluded at full text: 25
- Still awaiting a full text: 11

The first read used extracted methods and cue passages. Five records that read as uncertain, and the Chinese kinship paper, were checked again in the XML. Those checks included the Dual-Pathway Calibration Model scripts, the government-chatbot empathy scripts, the live-stream pronoun and emotional-word manipulation, the chatbot-anthropomorphism review section, and the ChatGPT emotional-expression section. The kinship paper stayed excluded: the interviews chart users’ resilience practices with generative “AI parents,” and they do not analyze linguistic features of the machine’s language.

The 21 inclusions are not a finished review set. They include scripted chatbot stimuli as well as live LLM output. Several operationalize cues in Chinese or Korean, so this partial set does not support a claim that the literature is English-only.

Publisher pages for the remaining 11 returned HTTP 403 or a bot challenge. They are not excluded for lack of a file.

## Not done

- ACL Anthology metadata filter
- Citation chasing
- Deduplication across sources
- Full text for 11 PubMed records and 15 *Human-Machine Communication* PDFs
- Evidence matrix
- Manuscript
