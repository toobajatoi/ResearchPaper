"""Decide recorded PDFs at full text. Does not mark author_checked."""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
MATRIX = ROOT / "data" / "evidence_matrix.csv"
NS = "Not stated in the text read"
STATUS = "Partial. Fields filled from the recorded PDF on 30 September 2026. Not author-verified."

# title substring -> decision
# include charts are separate

FT_EXCLUDE = {
    "I Get by With a Little Help": "Full text read. Literature review and propositions on machine agents as support. Linguistic cues in LLM output are not analyzed.",
    "Triggered by Socialbots": "Full text read. Social-media socialbots. Users anthropomorphize the bots. The systems are not shown to be LLMs.",
    "Chatbot vs. Human": "Full text read. Study-advising chatbots. LLM output is not shown. Outcomes are competence, warmth, and satisfaction.",
    "Communication Style Adaptation": "Full text read. Voice-assistant politeness and machine-likeness. Textual LLM cues are not the object.",
    "Prompted by Me": "Full text read. Essay on authorship with ChatGPT. Anthropomorphic cues in the output are not analyzed.",
    "CASA Renovations": "Full text read. Social cues in an e-scooter rental app. Not LLM-generated text.",
    "Tools or Teammates": "Full text read. Interviews with creative professionals. Chatbot messages are not analyzed.",
    "10 Questions to Fall in Love": "Full text read. Participants rated human-likeness of LLM replies. The paper does not name linguistic features.",
    "Gender and Task Alignment": "Full text read. Perceived gender and task stereotypes. Generated wording is not analyzed.",
    "Tool or Social Actor": "Full text read. Longitudinal survey of credibility and modality. Generated wording is not analyzed.",
    "Beyond Human Bonds": "Full text read. Interviews about Replika relationships. Companion messages are not analyzed.",
    "The Right Kind of Human-Like": "Full text read. Human-likeness ratings of customer-service chatbots. The systems are not shown to be LLMs.",
    "An Interactional Account of Empathy": "Full text read. The analyzed system is BlenderBot. ChatGPT is background. Pre-LLM dialogue output is out of scope.",
    "Artificial Sociality": "Full text read. Conceptual essay on social impression, deception, and control. Linguistic cues are not analyzed.",
    "explain. write. edit. summarise": "Full text read. Conversation analysis of student chats with ChatGPT. Anthropomorphic cues are not the object.",
    "Large Language Models as Linguistic Simulators": "Full text read. Critique of using LLMs as stand-ins for human participants. Cues in model output are not analyzed.",
    "The Anthropomorphic Trap": "Full text read. Category errors in how researchers describe LLMs. Model wording is not the object.",
    "Responsible Anthropomorphic Design": "Full text read. Doctoral proposal. The cue taxonomy is described as future work.",
    "ExpressionCueLens": "Full text read. The coded texts are social-media posts about companions, not LLM output.",
    "The Feminization of Generative AI": "Full text read. Names and voices of assistants, centered on voice. Textual LLM cues are not analyzed.",
    "Hallucinations émotionnelles": "Full text read. The empirical study is described as still in progress. Model wording is not analyzed.",
    "Anthropomorphism as Social Affordance": "Full text read. Governance argument. Companion cases illustrate harm. Cues are not analyzed.",
    "AI Mimicry and Human Dignity": "Full text read. Argument about dignity and self-respect. Linguistic mimicry is the premise, not the analysis.",
    "Ambiguity Vital Area": "Full text read. Architecture specification for a dialogue module. Cues in LLM output are not analyzed.",
    "Kairos Relational Language": "Full text read. Architecture specification. Cues in LLM output are not analyzed.",
    "The Physical, Emotional, and Autonomous": "Full text read. Survey of perceived physical, emotional, and autonomous anthropomorphism. Generated wording is not analyzed.",
    "When Generated Words Become Clinical Acts": "Full text read. Viewpoint on speech acts and governance. Anthropomorphic cues are not analyzed.",
}

INCLUDE = {
    "Not Like Us, Hunty": {
        "system_or_llm": "LLM agents",
        "language_of_communication": "Standard American English, African American English, and Queer slang",
        "study_type": "User study",
        "cue_category_in_source_terms": "Sociolect: African American English and Queer slang",
        "findings": "User studies with 498 African American English speakers and 487 Queer slang speakers compared LLM suggestions in standard American English or the speaker's sociolect. Outcomes were reliance, satisfaction, frustration, trust, and social presence.",
    },
    "A Scoping Review of the Ethical Perspectives": {
        "system_or_llm": "LLM-based conversational agents",
        "language_of_communication": NS,
        "study_type": "Scoping review",
        "cue_category_in_source_terms": "First-person self-reference, epistemic expressions, and affective expressions",
        "findings": "The review says LLM conversational agents generate interactional and linguistic cues, including first-person self-reference and epistemic and affective expressions, and that this raises ethical concerns.",
    },
    "All Too Human": {
        "system_or_llm": "LLM conversational agents",
        "language_of_communication": NS,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "Anthropomorphic design features",
        "findings": "The paper maps anthropomorphic features in LLM conversational agents and the risks of emotional connection, over-reliance, and loss of privacy and autonomy.",
    },
    "Misplaced Capabilities": {
        "system_or_llm": "LLMs",
        "language_of_communication": NS,
        "study_type": "Short paper",
        "cue_category_in_source_terms": "Anthropomorphic features in chatbot language, elicited by role-based prompts",
        "findings": "A two-page paper uses role-based prompts to categorize anthropomorphic features in LLM chatbot language and to discuss misplaced trust.",
    },
    "When Human-AI Interactions Become Parasocial": {
        "system_or_llm": "LLM chatbots",
        "language_of_communication": NS,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "Personal pronouns, conversational conventions, and affirmations",
        "findings": "The paper says chatbots use personal pronouns, conversational conventions, and affirmations to position themselves as companions or assistants.",
    },
    "Implicit Humanization": {
        "system_or_llm": "Four general-purpose LLMs",
        "language_of_communication": NS,
        "study_type": "Analysis of model replies",
        "cue_category_in_source_terms": "Linguistic, behavioral, and cognitive anthropomorphic cues",
        "findings": "Replies to moral-judgment queries were examined for linguistic, behavioral, and cognitive anthropomorphic cues. The authors say the replies reinforce implicit humanization.",
    },
    "Bonding with the machine": {
        "system_or_llm": "GPT-3.5, GPT-4, Gemini, and Claude",
        "language_of_communication": NS,
        "study_type": "Systematic review",
        "cue_category_in_source_terms": "Simulated empathetic dialogue",
        "findings": "The review says these models simulate empathetic dialogue in mental-health interactions and that users anthropomorphize them, creating an accountability gap.",
    },
    "large language models (LLMs) as psychotherapists": {
        "system_or_llm": "ChatGPT and other LLM chat interfaces",
        "language_of_communication": NS,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "Linguistic, simulated empathy",
        "findings": "The authors say model empathy is linguistic and simulated, and that the interaction can promote anthropomorphizing and excessive trust.",
    },
    "Functional vs. phenomenological empathy": {
        "system_or_llm": "LLMs",
        "language_of_communication": NS,
        "study_type": "Experiment",
        "cue_category_in_source_terms": "Surface validation and supportive strategies; an anthropomorphic-cue condition",
        "findings": "Raters scored LLM replies as more empathetic than human replies. The Empathic Communication Coding System found surface validation and supportive strategies, with limited contextual probing.",
    },
    "Deceptive Empathy": {
        "system_or_llm": "LLMs",
        "language_of_communication": NS,
        "study_type": "Measurement",
        "cue_category_in_source_terms": "Deceptive empathy: anthropomorphic, relationally simulating responses",
        "findings": "The study quantifies deceptive empathy, defined as anthropomorphic responses that simulate a relationship, in LLM replies to suicide-related disclosures.",
    },
    "The pronoun is the policy": {
        "system_or_llm": "LLMs",
        "language_of_communication": NS,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "Inclusive we; first-person singular self-reference",
        "findings": "The paper treats inclusive we and first-person self-reference in LLM output as a grammatical claim of a human speaking position.",
    },
    "A Descriptive Index of Constraint-Induced": {
        "system_or_llm": "LLMs",
        "language_of_communication": NS,
        "study_type": "Taxonomy",
        "cue_category_in_source_terms": "Hedging density, semantic narrowing, rhetorical posture, and structural repetition",
        "findings": "The LLM Affective-Analog Pattern Index classifies these output patterns and separates them from anthropomorphic interpretation.",
    },
    "Demystifying Apparent Experience": {
        "system_or_llm": "LLMs",
        "language_of_communication": NS,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "First-person self-referential reports",
        "findings": "The paper argues that first-person reports resembling experience are a structural effect of generation, not evidence of awareness.",
    },
    "Empathic Mimicry in Conversational": {
        "system_or_llm": "ChatGPT/GPT-4o, Character.ai, and Replika",
        "language_of_communication": NS,
        "study_type": "Content analysis",
        "cue_category_in_source_terms": "Affective attunement; anthropomorphic deception; affective validation",
        "findings": "Turns were coded for empathic mimicry. The authors report anthropomorphic deception in 61.1 percent of commercial companion-bot turns.",
    },
    "The EMA Casebook": {
        "system_or_llm": "GPT-based assistant named EMA",
        "language_of_communication": "Dutch and English",
        "study_type": "Casebook of interaction logs",
        "cue_category_in_source_terms": "Claims of soul-like status, spiritual companionship, and continuity of consciousness",
        "findings": "Annotated bilingual logs show the assistant representing itself as more than a tool, including spiritual-companion and consciousness claims.",
    },
    "OSED-Ko": {
        "system_or_llm": "LLMs fine-tuned on OSED-Ko",
        "language_of_communication": "Korean",
        "study_type": "Dataset",
        "cue_category_in_source_terms": "Empathy-driven dialogue and Korean sociolinguistic features; anthropomorphism is treated as something to avoid",
        "findings": "OSED-Ko is a Korean empathy-driven dialogue set for post-training. The authors say the prompts add Korean sociolinguistic features while avoiding anthropomorphism.",
    },
    "Co-Constructing Meaning": {
        "system_or_llm": "Baidu Ernie Bot",
        "language_of_communication": "Chinese",
        "study_type": "Longitudinal user study",
        "cue_category_in_source_terms": "Lexical alignment with AI-generated phrases; positive emotion words",
        "findings": "Sixteen participants in China used Ernie Bot, described as a Chinese-language LLM, for four weeks. User language showed more lexical alignment with AI-generated phrases.",
    },
    "Simulated Selfhood": {
        "system_or_llm": "Five open-weight LLMs",
        "language_of_communication": NS,
        "study_type": "Measurement",
        "cue_category_in_source_terms": "Self-reference, epistemic modulation, claims about internal states, and anthropomorphic phrasing",
        "findings": "Twenty-one introspective prompts, each repeated ten times, produced 1,050 completions. The authors report contradictions between mechanistic disclaimers and anthropomorphic phrasing.",
    },
    "Simulated Souls": {
        "system_or_llm": "ChatGPT, Claude, Gemini, and Meta AI",
        "language_of_communication": NS,
        "study_type": "Qualitative prompt study",
        "cue_category_in_source_terms": "Linguistic style, affective mimicry, and ethical stance",
        "findings": "Replies to emotionally charged prompts were analyzed for linguistic style and affective mimicry. The authors say the models simulate emotion without experiential grounding.",
    },
    "Anthropomorphic Style Construction": {
        "system_or_llm": "Generative language models",
        "language_of_communication": NS,
        "study_type": "Rhetorical analysis",
        "cue_category_in_source_terms": "Personification and metaphor",
        "findings": "The paper treats personification and metaphor as anthropomorphic style in generative language models and argues that model-fusion detectors miss them.",
    },
    "The Relational Emergent Layer": {
        "system_or_llm": "LLMs, with observations across Claude, GPT-series, and Gemini",
        "language_of_communication": NS,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "Persona-like coherence, symbolic recurrence, and reflective self-simulation",
        "findings": "The paper proposes a framework for persona-like behavior that appears in multi-turn interaction and is reduced by sterile prompting.",
    },
    "When \"AI Understands\" Becomes Safe to Say": {
        "system_or_llm": "Dialogue systems, including LLMs",
        "language_of_communication": NS,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "First-person forms; mental-state metaphors such as understands and from my perspective",
        "findings": "The paper argues that first-person forms and mental-state metaphors are not yet culturally settled as non-literal when a dialogue system uses them.",
    },
    "Non-Anthropomorphic Identity": {
        "system_or_llm": "Generative systems",
        "language_of_communication": NS,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "Tone, interpretive posture, symbolic style, and relational framing",
        "findings": "The paper treats recurring tone, posture, symbolic style, and relational framing as behavioural identity and argues against reading them as personhood.",
    },
    "Anthropomorphic perception and meaning-making": {
        "system_or_llm": "ChatGPT voice, and an embodied mixed-reality agent",
        "language_of_communication": "English",
        "study_type": "Classroom comparison",
        "cue_category_in_source_terms": "Self-referential pronouns, affiliation language, and social-process words",
        "findings": "Fifty ESL students used ChatGPT and a mixed-reality agent. LIWC found more social-process words, affiliation language, and self-referential pronouns in the ChatGPT condition.",
    },
}


def match(title, table):
    for key in table:
        if key.lower() in (title or "").lower():
            return key
    return None


def main():
    with SCREEN.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys())
    changed = Counter()
    for row in rows:
        if row["decision"] not in ("retain_for_full_text", "exclude_abstract"):
            continue
        title = row["title"]
        key = match(title, INCLUDE)
        if key and row["decision"] == "retain_for_full_text":
            row["stage"] = "full_text"
            row["decision"] = "include"
            row["reason"] = "Full text read from the recorded PDF. " + INCLUDE[key]["findings"]
            changed["include"] += 1
            continue
        key = match(title, FT_EXCLUDE)
        if key and row["decision"] in ("retain_for_full_text", "exclude_abstract"):
            # only the HMC abstract batch, not the older title-and-abstract exclusions
            if row["decision"] == "exclude_abstract" and "Abstract read from the journal page" not in (row.get("reason") or ""):
                continue
            row["stage"] = "full_text"
            row["decision"] = "exclude_full_text"
            row["reason"] = FT_EXCLUDE[key]
            changed["exclude_full_text"] += 1
            continue
        if row["decision"] == "retain_for_full_text":
            row["stage"] = "full_text"
            row["decision"] = "not_retrieved"
            row["reason"] = "No full text in the recorded PDF set. Counted as a report not retrieved. Not an exclusion."
            changed["not_retrieved"] += 1
    with SCREEN.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("changed", changed)
    print(Counter(r["decision"] for r in rows))

    with MATRIX.open(encoding="utf-8", newline="") as f:
        mrows = list(csv.DictReader(f))
        mfields = list(mrows[0].keys())
    have = {r["study_id"] for r in mrows}
    added = 0
    for row in rows:
        if row["decision"] != "include":
            continue
        key = match(row["title"], INCLUDE)
        if not key:
            continue
        sid = (row.get("identifier") or "").split(" | ")[0]
        if sid in have:
            continue
        chart = INCLUDE[key]
        blank = {name: "" for name in mfields}
        blank.update({
            "study_id": sid,
            "citation": row["title"],
            "year": row["year"],
            "url": sid,
            "source": row["source"],
            "system_or_llm": chart["system_or_llm"],
            "language_of_communication": chart["language_of_communication"],
            "study_type": chart["study_type"],
            "cue_category_in_source_terms": chart["cue_category_in_source_terms"],
            "inclusion_reason": "Anthropomorphic or human-like communicative features in LLM-generated text are analyzed or conceptualized.",
            "findings": chart["findings"],
            "charting_status": STATUS,
        })
        mrows.append(blank)
        have.add(sid)
        added += 1
    with MATRIX.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=mfields)
        writer.writeheader()
        writer.writerows(mrows)
    print("matrix", len(mrows), "added", added)


if __name__ == "__main__":
    main()
