from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from typing import List, Dict, Annotated


class GetMatchmakingResponse(BaseModel):
    matches: Dict[PositiveInt, PositiveInt]

class GetMatchmakingRequest(BaseModel):
    ids: List[PositiveInt] = Field(min_length=2, max_length=64)