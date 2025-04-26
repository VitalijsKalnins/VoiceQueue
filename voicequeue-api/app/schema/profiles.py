from pydantic import BaseModel, ConfigDict, StringConstraints, PositiveInt
from typing import List, Annotated
from app.enum.profiles import ProfileEntityType


class ProfileEntity(BaseModel):
    type: ProfileEntityType
    text: str
    subject: str
    sentiment: float
    model_config = ConfigDict(from_attributes=True)
    

## GET v1/profiles/{profile_id} Response
class GetProfileResponse(BaseModel):
    id: int
    text: str
    entities: List[ProfileEntity]
    model_config = ConfigDict(from_attributes=True)


class SetProfileRequest(BaseModel):
    id: PositiveInt
    text: Annotated[str, StringConstraints(min_length=32, max_length=252)]

class SetProfileResponse(BaseModel):
    success: bool
    model_config = ConfigDict(from_attributes=True)