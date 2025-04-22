from app.entity.profile import Profile, ProfileEntity
from app.core.config import settings
from app.logging.logger import logger
from app.nlp_tasks.NERSentimentV1 import NERSentimentV1
from app.nlp_tasks.EmbedderV1 import embed

## Import spaCy 
import spacy
from spacy_llm.registry import registry
from spacy.language import Language
from spacy.tokens import Doc

## Force spaCy to run on CUDA
spacy_cuda_available = spacy.prefer_gpu()
logger.info(f"spaCy CUDA available: {spacy_cuda_available}")

## Register NLP NER / Sentiment Task
@registry.llm_tasks("voicequeue.NER_SENTIMENT.v1")
def create_llm_task(labels: str = "INTEREST,DISINTEREST"):
    label_list = [l.strip() for l in labels.split(",")]
    return NERSentimentV1(labels=label_list)

## Register Embedder Component
@Language.component("EMBEDDER")
def create_component(doc: Doc):
    return embed(doc=doc)


class NLPService:
    def __init__(self):
        ## Create spaCy pipeline
        self.nlp = spacy.blank(settings.SPACY_MODEL)

        ## add_pipe NER / Sentiment Component
        self.nlp.add_pipe(
            "llm",
            config = {
                "task": {
                    "@llm_tasks": "voicequeue.NER_SENTIMENT.v1",
                },
                "model": {
                    "@llm_models": settings.SPACY_LLM_FAMILY,
                    "name": settings.SPACY_LLM_MODEL
                },
            }
        )
        ## add_pipe Embedder Component -> Designate to embed after NER / Sentiment Component
        self.nlp.add_pipe("EMBEDDER", last=True)

## NLP Service singleton
service = NLPService()
# doc = service.nlp("I love long walks on the beach and riding my horse, I am a cowboy! I absolutely despise aliens, I have a phobia of them.")
# for it in doc._.ner_sentiment_items:
#     logger.info(
#         f"TEXT='{it['text']}' | SUBJECT={it['subject']} | LABEL={it['label']} | SENTIMENT={float(it['sentiment']):+.2f} | EMBEDDING={it['embedding']}"
#     )