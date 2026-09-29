# Old project archive

**Status:** Discontinued. The files were deleted on 29 September 2026 at your request.

**Active project:** The scoping review in `SCOPING_REVIEW/`.

## What the old project was

The discontinued project was an original-data content analysis titled "Same Assistant, Different Voice? Anthropomorphic Communication Cues in Urdu and English Responses of Generative AI Assistants." It planned an API comparison of GPT, Claude, and Gemini in Urdu and English, with scenario prompts, a second coder, Krippendorff's alpha, and mixed-effects regression. That design is not being continued.

## Files deleted

| File | What it was |
| --- | --- |
| `master_prompt.txt` | Instructions for the discontinued content analysis. |
| `collect.py` | API collection script. |
| `collect_pilot_api.py` | Pilot API collection script. |
| `prompts.csv` | English and Urdu scenario prompts. |
| `prompts (1).csv` | Earlier copy of the prompts. |
| `translation_log.csv` | Log of Urdu wording changes. |
| `backtranslation_sheet.csv` | Back-translation sheet. The English column was empty. |
| `backtranslation_instructions.txt` | Instructions for that back-translation. |
| `raw_pilot_api.jsonl` | Logged API calls and model replies from the discontinued pilot. |
| `ai_use_log.csv` | Log of assistant work on the discontinued experiment. |
| `.env` | Local API credentials. Values were not copied anywhere before deletion. |
| `.env.example` | Blank credential template. |

## Kept

`.gitignore` still ignores `.env`, so a future credential file is not committed by accident.

`SCOPING_REVIEW/ai_use_log.md` is the log for the scoping review. It is separate from the deleted experiment log.

## Not in this folder

`collect_pilot_api.py` looked for `c:\Users\tooba\Downloads\collection_sheet.xlsx`. That workbook was never in this project folder, so it was not deleted from here.
