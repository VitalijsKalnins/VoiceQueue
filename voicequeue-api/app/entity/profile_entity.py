from app.enum.profiles import ProfileEntityType

## Imports for serializing / deserializing embedding field
from bson.binary import Binary
import pickle

class ProfileEntity:
    def __init__(
        self,
        text: str = "",
        type: ProfileEntityType = ProfileEntityType.UNKNOWN,
        sentiment: float = 0.0,
        embedding = None
    ):
        self.text = text
        self.type = type
        self.sentiment = sentiment
        self.embedding = embedding

    def to_dict(self):
        serialized = {
            "text": self.text,
            "type": self.type.value,
            "sentiment": self.sentiment,
            ## Serialize embeddding numpy array
            ## from https://stackoverflow.com/a/22194694
            "embedding": Binary(pickle.dumps(self.embedding, protocol=2), subtype=128)
        }
        return serialized
    
    def from_dict(serialized):
        deserialized = ProfileEntity(
            text = serialized.get("text"),
            type = ProfileEntityType(serialized.get("type")),
            sentiment = serialized.get("sentiment"),
            ## Deserialize embeddding numpy array
            ## from https://stackoverflow.com/a/22194694
            embedding = pickle.loads(serialized.get("embedding"))
        )
        return deserialized