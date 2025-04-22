from app.core.config import settings
from app.logging.logger import logger
from spacy.tokens import Doc
import numpy as np

## Import torch and SentenceTransformer
import torch
from sentence_transformers import SentenceTransformer

## Log torch CUDA availability
torch_cuda_available = torch.cuda.is_available()
logger.info(f"Torch CUDA available: {torch_cuda_available}")

## Initialize SentenceTransformer
embedder = SentenceTransformer(settings.EMBEDDING_MODEL, model_kwargs={"torch_dtype": "float16"}) 

## Embeds entities flagged by NER_SENTIMENT task
## Run after voicequeue.NER_SENTIMENT.v1 in the pipeline
def embed(doc: Doc):
    for it in doc._.ner_sentiment_items:
        it['embedding'] = embedder.encode(it['subject'], convert_to_numpy=True)
    return doc

## Returns the cosine similarity matrix of embeddings_a and embeddings_b
## Converts from nparray to torch tensors residing on the GPU
def similarity(embedding_a, embedding_b):
    torch_embedding_a = torch.as_tensor(np.array(embedding_a))
    torch_embedding_b = torch.as_tensor(np.array(embedding_b))
    return embedder.similarity(torch_embedding_a, torch_embedding_b)