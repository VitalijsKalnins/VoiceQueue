from pydantic import BaseModel, ConfigDict
from typing import List
from app.enum.profiles import ProfileEntityType


class ProfileEntity(BaseModel):
    type: ProfileEntityType
    text: str
    sentiment: float
    model_config = ConfigDict(from_attributes=True)
    

## GET v1/profiles/{profile_id} Response
class GetProfileResponse(BaseModel):
    id: int
    text: str
    entities: List[ProfileEntity]
    model_config = ConfigDict(from_attributes=True)