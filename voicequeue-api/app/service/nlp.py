from app.entity.profile import Profile, ProfileEntity
from app.enum.profiles import ProfileEntityType
from app.core.config import settings
from app.logging.logger import logger
from app.nlp_tasks.NERSentimentV1 import NERSentimentV1
from app.nlp_tasks.EmbedderV1 import embed, similarity

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

    ## Runs text through pipeline, extracts profile entities -> returns profile
    def extract_entities(self, input: str) -> Profile:
        ## to-do: some input validation stuff here
        doc = self.nlp(input)

        ## Label -> ProfileEntityType Map
        label_map = {
            "INTEREST": ProfileEntityType.INTEREST,
            "DISINTEREST": ProfileEntityType.DISINTEREST
        }

        ## Initialize list to hold profile entity objs. for profile
        profile_entities = []
        for item in doc._.ner_sentiment_items:
            ## Create new ProfileEntity
            extracted_entity = ProfileEntity(
                text = item["text"],
                subject = item["subject"],
                type = label_map.get(item["label"], ProfileEntityType.UNKNOWN),
                sentiment = item["sentiment"],
                embedding = item["embedding"]
            )
            profile_entities.append(extracted_entity)

        ## Create new Profile
        res_profile = Profile(
            ## Id is assigned on the Profile service
            id = -1,
            text = input,
            entities = profile_entities
        )
        return res_profile
    
    ## Processes and returns the cosine similarity matrix of two given Profiles
    def similarity_matrix(self, profile_a: Profile, profile_b: Profile):
        ## Fetch profile entity embeddings for both profiles
        embeddings_a = [profile_ent.embedding for profile_ent in profile_a.entities]
        embeddings_b = [profile_ent.embedding for profile_ent in profile_b.entities]

        ## Compute and return similarity matrix
        return similarity(embeddings_a, embeddings_b)


## NLP Service singleton
service = NLPService()

# embeddings_a, embeddings_b = [profile_ent.embedding for profile_ent in profile1.entities], [profile_ent.embedding for profile_ent in profile2.entities]
# similarities = similarity(embeddings_a, embeddings_b)

# for id_x, profile_x in enumerate(profile1.entities):
#     for id_y, profile_y in enumerate(profile2.entities):
#         logger.info(f"profile_x entity: {profile_x.text}, profile_y entity: {profile_y.text}, similarity: {similarities[id_x][id_y]}")