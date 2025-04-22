from app.core.config import settings
from app.logging.logger import logger
from spacy.tokens import Doc

## Import torch and SentenceTransformer
import torch
from sentence_transformers import SentenceTransformer
logger.info(f"Torch CUDA available: {torch.cuda.is_available()}")

## Initialize SentenceTransformer
embedder = SentenceTransformer(settings.EMBEDDING_MODEL, model_kwargs={"torch_dtype": "float16"}) 

def embed(doc: Doc):
    for it in doc._.ner_sentiment_items:
        it['embedding'] = embedder.encode(it['text'], convert_to_numpy=True)
    return doc