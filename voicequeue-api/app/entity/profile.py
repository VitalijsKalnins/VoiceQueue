from typing import Optional, List
from app.entity.profile_entity import ProfileEntity

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

    def to_dict(self):
        serialized = {
            "_id": self.id,
            "text": self.text,
            "entities": [entity.to_dict() for entity in self.entities]
        }
        return serialized
    
    def from_dict(serialized):
        deserialized = Profile(
            id = serialized.get("_id"),
            text = serialized.get("text"),
            entities = [ProfileEntity.from_dict(entity) for entity in serialized.entities]
        )
        return deserialized