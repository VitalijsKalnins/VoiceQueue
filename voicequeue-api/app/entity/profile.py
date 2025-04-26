from typing import Optional, List, Dict, Self
from app.entity.profile_entity import ProfileEntity

from typing import Dict

class Profile:
    def __init__(
        self,
        id: int = 0,
        text: str = "",

        ## This is only optional for the constructor param,
        ## defaults to empty list at runtime if not provided
        entities: Optional[List[ProfileEntity]] = None,
    ):
        self.id = id
        self.text  = text
        
        ## Initialize as empty list if profile entity list is not passed
        self.entities: List[ProfileEntity] = entities or []

    def to_dict(self) -> Dict:
        serialized = {
            "_id": self.id,
            "text": self.text,
            "entities": [entity.to_dict() for entity in self.entities]
        }
        return serialized
    
    def to_response_dict(self) -> Dict:
        serialized = {
            "id": self.id,
            "text": self.text,
            "entities": [entity.to_response_dict() for entity in self.entities]
        }
        return serialized
    
    @staticmethod
    def from_dict(serialized: Dict) -> Self:
        deserialized = Profile(
            id = serialized.get("_id"),
            text = serialized.get("text"),
            entities = [ProfileEntity.from_dict(entity) for entity in serialized.get("entities")]
        )
        return deserialized