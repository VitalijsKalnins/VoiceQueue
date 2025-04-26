from app.enum.profiles import ProfileEntityType
from typing import Dict, Self

## Imports for serializing / deserializing embedding field
from bson.binary import Binary
import pickle

class ProfileEntity:
    def __init__(
        self,
        text: str = "",
        subject: str = "",
        type: ProfileEntityType = ProfileEntityType.UNKNOWN,
        sentiment: float = 0.0,
        embedding = None
    ):
        self.text = text
        self.subject = subject
        self.type = type
        self.sentiment = sentiment
        self.embedding = embedding

    def to_dict(self) -> Dict:
        serialized = {
            "text": self.text,
            "subject": self.subject,
            "type": self.type.value,
            "sentiment": self.sentiment,
            ## Serialize embeddding numpy array
            ## from https://stackoverflow.com/a/22194694
            "embedding": Binary(pickle.dumps(self.embedding, protocol=2), subtype=128)
        }
        return serialized
    
    def to_response_dict(self) -> Dict:
        serialized = {
            "text": self.text,
            "subject": self.subject,
            "type": self.type.value,
            "sentiment": self.sentiment,
        }
        return serialized
    
    @staticmethod
    def from_dict(serialized) -> Self:
        deserialized = ProfileEntity(
            text = serialized.get("text"),
            subject = serialized.get("subject"),
            type = ProfileEntityType(serialized.get("type")),
            sentiment = serialized.get("sentiment"),
            ## Deserialize embeddding numpy array
            ## from https://stackoverflow.com/a/22194694
            embedding = pickle.loads(serialized.get("embedding"))
        )
        return deserialized