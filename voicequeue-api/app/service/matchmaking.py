from app.service.profiles import service as ProfileService
from app.service.nlp import service as NLPService
from app.entity.profile import Profile
from app.logging.logger import logger

from typing import List, Dict

## NetworkX Matchmaking imports
from networkx import complete_graph, to_undirected, max_weight_matching

class MatchmakingService:
    def __init__(self, similarity_alpha: float, relative_alpha_factor: float, opposing_sentiment_factor: float):
        ## Similarity Alpha Threshold [float(0 .. 1)]
        ## profile entities must be >= SIMILARITY_ALPHA to be
        ## factored in compatibility computations
        self.SIMILARITY_ALPHA = similarity_alpha

        ## Factor for compatibility score relativity to threshold alpha [float]
        ## dependant on similarity strength from the threshold alpha
        self.RELATIVE_ALPHA_FACTOR = relative_alpha_factor

        ## Factor for compatibility score opposing sentiment calculations [float]
        self.OPPOSING_SENTIMENT_FACTOR = opposing_sentiment_factor

    ## Computes compatibility between profileA and profileB
    ## Note: this must be an integer for max_weight_matching algo accuracy
    def compute_compatibility(self, profileA: Profile, profileB: Profile) -> int:
        ## Initialize score
        score: int = 0

        ## Fetch similarity matrix between profile entities of profileA and profileB
        similarity_matrix = NLPService.similarity_matrix(profileA, profileB)

        ## Iterate through profile entities between both profiles,
        ## adjust score based on sentiment IF similarity of both
        ## entities is >= SIMILARITY_ALPHA
        for idx, profileA_ent in enumerate(profileA.entities):
            for idy, profileB_ent in enumerate(profileB.entities):
                ## fetch entity similarity from similarity matrix
                ent_similarity = similarity_matrix[idx][idy].item()
                ent_similarity_normalized = round(ent_similarity * 100)

                ## Calculate relative alpha 0 -> 1
                ## closer to similarity threshold, approaches 0; further to similarity threshold, approaches 1
                ## this is used to further increment / decrement score based on similarity strength from the threshold alpha
                relative_alpha = (ent_similarity - self.SIMILARITY_ALPHA) / (1 - self.SIMILARITY_ALPHA)

                if (ent_similarity >= self.SIMILARITY_ALPHA):
                    ## IF the entity type (INTERTEST | DISINTEREST) matches
                    ## increment score by average of both profile entity sentiments multiplied by similarity
                    ## ELSE decrement score by absolute difference in both profile entity
                    ## sentiments multiplied by similarity
                    if (profileA_ent.type == profileB_ent.type):
                        avg_sentiment = ((profileA_ent.sentiment + profileB_ent.sentiment) / 2)
                        score += round((avg_sentiment * ent_similarity_normalized) + (relative_alpha * ent_similarity_normalized * self.RELATIVE_ALPHA_FACTOR))
                    else:
                        delta_sentiment = abs(profileA_ent.sentiment - profileB_ent.sentiment)
                        score -= round((delta_sentiment * ent_similarity_normalized * self.OPPOSING_SENTIMENT_FACTOR) + (relative_alpha * ent_similarity_normalized * self.RELATIVE_ALPHA_FACTOR))

        return score

    ## Matchmake users, ensuring maximal weight compatibility possible
    ## Constructs complete graph, assigns compatibility weights -> performs max_weight_matching
    ## Converts matched user pairs to dictionary
    async def matchmake(self, users: List[int]) -> Dict:
        res: Dict = {}

        ## Ensure we have an even number of users to matchmake
        ## to-do:

        ## Create the completely connected undirected graph of users
        user_graph = to_undirected(complete_graph(users))

        ## Fetch all user profiles from profile service
        user_to_profile = await ProfileService.get_profiles(users)

        ## Assign weights of each user -> user edge with their profile compatibility
        for edge in user_graph.edges.data():
            profileA = user_to_profile[edge[0]]
            profileB = user_to_profile[edge[1]]
            edge[2]["weight"] = self.compute_compatibility(profileA, profileB)
            logger.info(f"({profileA.id})<-->({profileB.id}) Computed Compatibility: {edge[2]['weight']}")

        ## Perform max weight matching
        matches = max_weight_matching(user_graph, maxcardinality=True)
        
        ## Construct resulting dictionary from matches
        for match in matches:
            res[match[0]] = match[1]

        return res

## Matchmaking Service Singleton
service = MatchmakingService(similarity_alpha = 0.28, relative_alpha_factor = 1, opposing_sentiment_factor = 0.5)