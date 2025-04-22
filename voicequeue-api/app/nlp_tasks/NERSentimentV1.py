from typing import Iterable, List, Dict, Any
import srsly

## Set Doc extension for task
from spacy.tokens import Doc
Doc.set_extension("ner_sentiment_items", default=[], force=True)

class NERSentimentV1:
    ## LLM Task Prompt
    PROMPT = """\
    You are a INTEREST / DISINTEREST Classifier and Sentiment analyzer, you must:
    Extract every phrase that expresses a personal INTEREST or DISINTEREST of a given SUBJECT from the text within:<<<>>>.
    Return a JSON array where each item is:
    {{
        "text":       <phrase expressing INTEREST / DISINTEREST  for a SUBJECT>,
        "subject"     <SUBJECT of INTEREST / DISINTEREST>,
        "label":      "INTEREST" | "DISINTEREST",
        "sentiment":  <float between -1 and 1>
    }}
    If a given phrase contains more than one INTEREST / DISINTEREST, create a separate item by extrapolating the phrase.
    i.e: 'I love programming and music' should be converted to two separate items where the phrases would be: 'I love programming', 'I love music'.
    INTERESTS / DISINTERESTS must strictly contain a SUBJECT the INTEREST / DISINTEREST is referring to.
    Do not include additional comments as separate items, only capture the main classification of a given subject.
    i.e: 'I slightly dislike apples, but overall they're not bad!' should only classify the phrase 'I slightly dislike apples.' while ignoring the additional comment.
    If a given phrase contains an expression regarding a belief or expresses feeling towards a sense of being regarding a subject, classify this accordingly.
    i.e: 'I believe that aliens are real.' should classify the subject as 'belief in alien existence'.
    i.e: 'I am a cowboy.' should classify the subject as 'is a cowboy'.
    ONLY Return the JSON array, do not wrap the JSON array in any markdown or syntax such as ```json ... ```.
    Text: <<<{{text}}>>>
    """
    def __init__(self, labels):
        self.labels = labels

    def generate_prompts(self, docs: Iterable[Doc]) -> Iterable[str]:
        for doc in docs:
            yield self.PROMPT.replace("{{text}}", doc.text)

    def parse_responses(self, docs: Iterable[Doc], responses: Iterable[str]) -> Iterable[Doc]:
        for doc, raw in zip(docs, responses):
            try:
                items: List[Dict[str, Any]] = srsly.json_loads(raw[0])
            except Exception:
                items = []
            doc._.ner_sentiment_items = items
            yield doc