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

## PubMed Search 2 and CASA extra

Both were run on 29 September 2026. Search 2 returned **80** records, of which 32 were already in Search 1. The CASA extra query returned **11**, of which 4 were already in Search 1. New records are in `data/screening.csv`.

Of the 48 Search 2 records that were not already in Search 1: 43 were excluded at title, 2 were excluded at abstract, and 3 were kept for full text (Japanese workplace politeness and honorifics, PMID 42507678; culturally aware prompting and politeness, PMID 42277102; French and German address pronouns, PMID 35071147). The 7 new CASA-extra records were excluded at title. None of these is an included study yet.

## ACL Anthology

The public abstracts file `anthology+abstracts.bib.gz` was downloaded on 29 September 2026 (42,441,419 bytes) and filtered locally. The Anthology website search is Google Custom Search and was not used as the count.

Records from 2020 through 2026 whose title or abstract matched Search 1: **614**. Title screening kept **49** for abstract reading and excluded **564**. One of the 614, Cheng et al. (2025), was read in full from the open text and included, so it is not in the 49. Search 2 on the same file returned **210** before deduplication with Search 1. Those 210 have not been added as a separate screened set.

## Open full texts read

These were read from arXiv HTML and included:

- DeVrio, Cheng, Egede, Olteanu, and Blodgett (2025), DOI 10.1145/3706598.3714038
- Ibrahim et al., arXiv 2502.07077
- Cheng, Blodgett, DeVrio, Egede, and Olteanu (2025), DOI 10.18653/v1/2025.acl-long.1259
- Shanahan, McDonell, and Reynolds (2023), PMID 37938776, arXiv 2305.16367

## ACL abstracts

On 29 September 2026 the 49 ACL Search 1 titles that had been kept were read at abstract. **10** were kept for full text. **39** were excluded at abstract. Cheng et al. (2025) was already included and was not counted again. None of the 10 is an included study. The reasons are in `data/screening.csv`.

## Who screened

Title, abstract, and full-text decisions in this log were assisted by the Cursor agent. The author has not yet checked them. `data/author_verification_sample.csv` lists every included study and a random 10 percent of the exclusions, drawn with seed 20260929 after the records below were added. The Preregistered badge will not be requested. Screening began on 29 September 2026, before any OSF deposit.

## OpenAlex as the multidisciplinary index

Scopus and Web of Science were dropped on 29 September 2026 because this review has no subscription.

The wide OpenAlex Search 1 count remains **11,245**. Dropping chatbot terms but keeping "human-like" and "social presence" still returned **7,330**. The exported query requires an anthropomorphism stem and an LLM or generative-AI term, in title and abstract, from 2020-01-01 through 2026-09-29. OpenAlex reported **1,411**. All 1,411 records were saved. Three DOIs were already in the screening log. The other **1,408** were added as records whose abstracts have not been read. They are not inclusions.

## IEEE Xplore and ACM

The IEEE Xplore website search was run on 29 September 2026 with the same anthropomorphism and LLM terms, years 2020–2026. It returned **70** records. Twenty-one were already in the log. Of the 49 new records, **9** were kept for abstract reading and **40** were excluded at title. None is included.

The ACM Digital Library website returned HTTP 403, a bot challenge. It was not searched. Those 403 records are not an ACM result set.

## Citation chasing of the four seed papers

OpenAlex was asked, on 29 September 2026, for references and citing papers. These lists are saved and have not been screened.

- DeVrio et al. (2025): 66 references saved; 29 citing papers saved (OpenAlex cited-by count 28).
- Cheng et al. (2025): OpenAlex returned no reference list; 8 citing papers saved (cited-by count 7).
- Shanahan et al. (2023): 13 references saved; the first 200 of 454 citing papers were saved.
- Ibrahim et al. (arXiv 2502.07077): OpenAlex returned no reference list; 8 citing papers saved.

## Evidence matrix

`data/evidence_matrix.csv` has one row for each of the 27 included studies. Most cells are empty. The filled cells come from the full-text decision notes. This is not a finished extraction.

A second request for one *Human-Machine Communication* PDF, Concannon et al. (2023), using a browser user agent, returned HTTP 403. The 15 journal PDFs remain unread. They are not excluded for lack of a file.

Two PubMed full texts were read from open PDFs and included. Ollier, Nißen, and von Wangenheim (2022), PMID 35071147, manipulated French *tu/vous* and German *du/Sie* in a rule-based text chatbot and measured humanlike ratings. Gao and colleagues (2026), PMID 42507678, had native raters score Japanese politeness and honorifics in LLM workplace replies. The authors call this cultural alignment, not anthropomorphism. Shen and colleagues, PMID 42277102, and the other unread PubMed papers are still unread.

## Recheck of suspicious exclusions

On 29 September 2026 the exclusion sample was checked against the papers, not only the titles. Three ACL title exclusions were reopened for full text and were not marked included: Cheng, Yu, and Jurafsky (2025), HumT DumT; Vanderlyn and colleagues (2021), which is a pre-LLM agent and still depends on the scope decision; and Kim and colleagues (2026) on affective hallucination. Personality expressed in generated wording is now an inclusion rule in the protocol. That reopened the psychometric personality paper and P-React. Backchannels and fillers (ACL 2026) were also reopened. Ward and colleagues on character traits, Wang and colleagues on detecting human-like text, and Lloyd on machine sentience stay excluded.

A broader keyword pass over the 564 ACL title exclusions produced 82 extra titles. Most name human-like reasoning, memory, syntax, vision, or translation. Those stayed excluded. Seventeen titles that name role-play, personality, emotion in dialogue, attachment language, or backchannels were returned to abstract screening.

INTIMA (Kaffee, Pistilli, and Jernite; arXiv 2508.09998; the PDF carries a 2026 AAAI copyright line) was missing from the search. It is in the screening log for full text. It is not included yet.

`author_checked` is still blank.

## Not done

- ACM Digital Library, after the website block
- Abstract screening of the 1,408 new OpenAlex records and the 9 new IEEE titles
- Screening the citation-chase lists
- Full text for 10 remaining PubMed Search 1 records, 1 remaining Search 2 record (PMID 42277102), 15 *Human-Machine Communication* PDFs, and 10 ACL papers kept at abstract
- Author verification of the included studies and the exclusion sample
- A complete evidence matrix
- Manuscript
