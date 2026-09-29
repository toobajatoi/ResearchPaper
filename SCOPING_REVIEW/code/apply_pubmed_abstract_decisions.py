"""Apply abstract-level decisions to PubMed records kept after the title screen.

Decisions were made from the abstracts in data/pubmed/retained_abstracts.json.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"

# PMID -> (decision, reason)
DECISIONS = {
    "42792503": (
        "retain_for_full_text",
        "Systematic review of conversational AI as a social actor, using the Computers Are Social Actors paradigm.",
    ),
    "42783578": (
        "exclude_abstract",
        "Reviews large language models as creativity-scoring tools. It does not analyze anthropomorphic communication cues.",
    ),
    "42753507": (
        "exclude_abstract",
        "Measures anthropomorphism as one global perception among other attributes. It does not identify linguistic cues.",
    ),
    "42726769": (
        "retain_for_full_text",
        "Compares visual anthropomorphism with social conversation cues in live-stream chatbots.",
    ),
    "42721382": (
        "retain_for_full_text",
        "Argues that fluent, empathic conversational-AI replies lead users to treat systems as social entities.",
    ),
    "42712761": (
        "retain_for_full_text",
        "Conceptual account of anthropomorphism in human-AI companionship.",
    ),
    "42651447": (
        "retain_for_full_text",
        "Experiments manipulate anthropomorphic cues and trace a social-closeness pathway.",
    ),
    "42648233": (
        "retain_for_full_text",
        "Review of design-based and individual anthropomorphism of AI, including chatbots.",
    ),
    "42631053": (
        "exclude_abstract",
        "Uses anthropomorphism as a predictor of older adults' intention to adopt a chatbot.",
    ),
    "42600040": (
        "exclude_abstract",
        "Models social presence as a moderator of travel-chatbot relationships. It does not specify communicative cues.",
    ),
    "42564617": (
        "exclude_abstract",
        "Links a global anthropomorphism score to belongingness. It does not analyze linguistic features.",
    ),
    "42549111": (
        "retain_for_full_text",
        "Manipulates first-person versus third-person framing and text versus speech in a large language model.",
    ),
    "42528981": (
        "retain_for_full_text",
        "Scoping review of human-like companion conversational agents and socioaffective mechanisms.",
    ),
    "42510216": (
        "retain_for_full_text",
        "Tests chatbot empathy as a communicative feature under social-presence theory.",
    ),
    "42487918": (
        "retain_for_full_text",
        "Reviews social roles and human-likeness in persuasive large language models.",
    ),
    "42482727": (
        "retain_for_full_text",
        "Interviews Chinese users about kinship terms and parent-like chatbots.",
    ),
    "42463863": (
        "retain_for_full_text",
        "Models healthcare-chatbot anthropomorphism, with data from users in Pakistan.",
    ),
    "42272711": (
        "exclude_abstract",
        "Uses perceived anthropomorphism to predict adoption of healthcare chatbots.",
    ),
    "42269974": (
        "retain_for_full_text",
        "Conceptualizes sycophancy and anthropomorphic projection in generative-AI mental-health support.",
    ),
    "42259210": (
        "exclude_abstract",
        "Uses perceived anthropomorphism to predict purchase behavior.",
    ),
    "42198871": (
        "exclude_abstract",
        "Measures perceived social presence as a predictor of isolation. It does not analyze message cues.",
    ),
    "42053557": (
        "exclude_abstract",
        "No abstract was available. The record is a legal-accountability commentary, not a cue analysis.",
    ),
    "42042227": (
        "retain_for_full_text",
        "Manipulates appearance anthropomorphism and empathic responses in medical conversational agents.",
    ),
    "42022410": (
        "exclude_abstract",
        "Uses anthropomorphism as a predictor of students' adoption of conversational AI.",
    ),
    "41783300": (
        "exclude_abstract",
        "Compares human-like avatars and names. It does not analyze linguistic cues.",
    ),
    "41750087": (
        "retain_for_full_text",
        "Tests five days of friendlike conversation with an AI chatbot and measures perceived empathy and anthropomorphism.",
    ),
    "41705167": (
        "retain_for_full_text",
        "Studies AI-anchor anthropomorphism beyond physical appearance in live streaming that uses large language models.",
    ),
    "41663521": (
        "retain_for_full_text",
        "Interviews in Pakistan and China on human-like cues, empathy, personalization, and social presence.",
    ),
    "41632953": (
        "retain_for_full_text",
        "Tests message humanness as the feature that leads women to perceive a health chatbot as human.",
    ),
    "41548427": (
        "retain_for_full_text",
        "Reviews whether therapy chatbots empathize and how empathetic design is claimed.",
    ),
    "41394040": (
        "retain_for_full_text",
        "Distinguishes functional and interactional anthropomorphism in generative AI.",
    ),
    "41346507": (
        "exclude_abstract",
        "Uses an anthropomorphism scale to predict adolescents' exercise motivation.",
    ),
    "41315393": (
        "retain_for_full_text",
        "Tests matching an embodied agent's appearance to the emotional tone of its message.",
    ),
    "41308091": (
        "exclude_abstract",
        "Measures social presence through gestures and a listening-recall task, not textual cues.",
    ),
    "41294639": (
        "retain_for_full_text",
        "Blind comparison of GPT-generated and clinician discharge texts on empathy and human wording.",
    ),
    "41234618": (
        "retain_for_full_text",
        "Designs human-like counseling dialogue for Korean-speaking adolescents and young adults.",
    ),
    "41120331": (
        "exclude_abstract",
        "Tests an individual-difference anthropomorphism scale as a predictor of social connection.",
    ),
    "41062558": (
        "retain_for_full_text",
        "Treats human-like empathy and warmth as features of generative-AI chatbots.",
    ),
    "41060458": (
        "retain_for_full_text",
        "Review of visual and linguistic anthropomorphism in chatbots.",
    ),
    "40873934": (
        "exclude_abstract",
        "Uses anthropomorphic tendency as a moderator of problematic conversational-AI use.",
    ),
    "40851577": (
        "retain_for_full_text",
        "Review of when interaction with artificial agents resembles human interaction, including social presence.",
    ),
    "40810905": (
        "retain_for_full_text",
        "Patients rate empathy, compassion, and self-disclosure in replies from a GPT-4 medical chatbot.",
    ),
    "40703735": (
        "retain_for_full_text",
        "Experiments on how anthropomorphic cues and source labels change evaluations of emotionally significant messages.",
    ),
    "40694494": (
        "retain_for_full_text",
        "Conceptual analysis of attributing human epistemic trust to conversational AI.",
    ),
    "40588891": (
        "exclude_abstract",
        "Proposes an empathic-chatbot architecture. It does not analyze existing communicative cues.",
    ),
    "40562106": (
        "retain_for_full_text",
        "Compares a text-only chatbot with a chatbot that adds voice and animation as social cues.",
    ),
    "40415069": (
        "retain_for_full_text",
        "Measures users' attributions of consciousness and other mental states to a large language model.",
    ),
    "40378006": (
        "retain_for_full_text",
        "Defines anthropomorphic conversational agents as systems that mimic human communication.",
    ),
    "40286349": (
        "retain_for_full_text",
        "Compares Gen-Z slang with standard language in an educational chatbot and measures perceived human-likeness.",
    ),
    "40271364": (
        "retain_for_full_text",
        "Reviews how chatbots, avatars, and robots shape attributions of mental states.",
    ),
    "40160265": (
        "retain_for_full_text",
        "Finds cultural differences in bonding with chatbots, explained by a greater tendency to anthropomorphize technology among East Asian participants.",
    ),
    "40123640": (
        "retain_for_full_text",
        "Conceptual paper on anthropomorphism of language-based chatbots in education.",
    ),
    "40001748": (
        "exclude_abstract",
        "Tests proactive replies and emoji use as predictors of purchase intention.",
    ),
    "39919295": (
        "exclude_abstract",
        "Compares chatbots on correction of cognitive biases. It does not analyze anthropomorphic cues.",
    ),
    "39661968": (
        "retain_for_full_text",
        "Systematic review of empathy in large language model outputs.",
    ),
    "39636606": (
        "exclude_abstract",
        "Tests a trust model and personalization. It does not analyze anthropomorphic language.",
    ),
    "39631034": (
        "retain_for_full_text",
        "Argues against sentience claims and against anthropomorphic language in NLP reporting.",
    ),
    "39526123": (
        "retain_for_full_text",
        "Reinterprets the Eliza effect in social chatbot relationships.",
    ),
    "39359701": (
        "exclude_abstract",
        "Compares a video avatar with a text chatbot on trust in breast-reconstruction answers.",
    ),
    "39226544": (
        "retain_for_full_text",
        "Builds a taxonomy of social communication, affiliation, and presence features in eHealth apps.",
    ),
    "39116598": (
        "exclude_abstract",
        "Studies how exposure to large language models changes people's view of uniquely human traits.",
    ),
    "39055534": (
        "retain_for_full_text",
        "Tests the gender of virtual chatbots as a cue in human-machine communication.",
    ),
    "39012688": (
        "retain_for_full_text",
        "Scoping review of conversational agents, voicebots, and anthropomorphic avatars as human-like carers.",
    ),
    "38958218": (
        "retain_for_full_text",
        "Critical analysis of the humanization of large language model conversational agents.",
    ),
    "38957452": (
        "retain_for_full_text",
        "Reviews ChatGPT's human-like conversational responses from human-computer interaction and psychology.",
    ),
    "38683664": (
        "exclude_abstract",
        "Compares a visual digital human with a text chatbot on usability, not on linguistic cues.",
    ),
    "38618488": (
        "retain_for_full_text",
        "Surveys attributions of phenomenal consciousness to large language models.",
    ),
    "38565880": (
        "retain_for_full_text",
        "Measures human-like personality traits of ChatGPT as features that affect knowledge sharing.",
    ),
    "38528008": (
        "retain_for_full_text",
        "Primes chatbots with emotional scenarios and examines human-like response patterns.",
    ),
    "38510306": (
        "retain_for_full_text",
        "Tests whether mind perception changes acceptance of emotional versus informational chatbot support.",
    ),
    "38428201": (
        "retain_for_full_text",
        "Scoping review of human-like communication techniques in healthcare conversational agents.",
    ),
    "38238474": (
        "retain_for_full_text",
        "Audits GPT-3 dialogues with participants who differ in gender, race, education, and viewpoint.",
    ),
    "38064707": (
        "retain_for_full_text",
        "Scoping review of embodied conversational agents, including appearance, dialogue mechanism, and emotional model.",
    ),
    "37952037": (
        "exclude_abstract",
        "Replicates the Computers Are Social Actors study on desktop computers. It does not study generative language systems.",
    ),
    "37938776": (
        "retain_for_full_text",
        "Proposes role play as a way to describe human-like dialogue agents without ascribing human traits.",
    ),
    "37561567": (
        "retain_for_full_text",
        "Manipulates anthropomorphic cues of healthcare conversational agents, including appearance. Full text is needed to see whether linguistic cues are included.",
    ),
    "37503997": (
        "exclude_abstract",
        "Uses a voice assistant to administer a questionnaire. Textual communication cues are not analyzed.",
    ),
    "37057977": (
        "exclude_abstract",
        "Manipulates a human face versus a robot face. The anthropomorphism is visual.",
    ),
    "36101883": (
        "retain_for_full_text",
        "Designs a learning-buddy chatbot from a social-presence framework that includes interpersonal communication.",
    ),
    "35976080": (
        "retain_for_full_text",
        "Tests friendly language in a product-recommendation chatbot using the Computers Are Social Actors and social-presence theories.",
    ),
    "35903740": (
        "exclude_abstract",
        "Describes behavior-change techniques delivered by an anthropomorphic agent. It does not analyze communicative cues.",
    ),
    "35802407": (
        "retain_for_full_text",
        "Systematic review of language use in conversational-agent health communication.",
    ),
    "34957013": (
        "exclude_abstract",
        "Voice-assistant study of loneliness. Textual cues are not available for analysis.",
    ),
    "34870266": (
        "exclude_abstract",
        "Measures users' tendency to anthropomorphize and felt connection. It does not identify message cues.",
    ),
    "33913814": (
        "retain_for_full_text",
        "Reviews personalization of conversational-agent interaction styles, including anthropomorphic cues.",
    ),
    "33842700": (
        "exclude_abstract",
        "Compares a monologue embodied agent with on-screen text as motivational formats, not as anthropomorphic language.",
    ),
}


def main():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    missing = []
    updated = 0
    for row in rows:
        if row["source"] != "PubMed supplementary Search 1":
            continue
        if row["decision"] != "retain_for_abstract":
            continue
        pmid = row["identifier"].replace("PMID:", "")
        if pmid not in DECISIONS:
            missing.append(pmid)
            continue
        decision, reason = DECISIONS[pmid]
        row["stage"] = "abstract"
        row["decision"] = decision
        row["reason"] = reason
        updated += 1
    if missing:
        raise SystemExit(f"missing decisions: {missing}")
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    retained = sum(1 for row in rows if row["decision"] == "retain_for_full_text" and row["source"].startswith("PubMed"))
    excluded = sum(1 for row in rows if row["decision"] == "exclude_abstract" and row["source"].startswith("PubMed"))
    print(f"updated {updated}; pubmed full-text queue {retained}; excluded at abstract {excluded}")


if __name__ == "__main__":
    main()
