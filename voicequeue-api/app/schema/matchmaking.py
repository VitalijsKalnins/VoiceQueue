from pydantic import BaseModel, Field, PositiveInt
from typing import List, Dict


class GetMatchmakingResponse(BaseModel):
    matches: Dict[PositiveInt, PositiveInt]

class GetMatchmakingRequest(BaseModel):
    ids: List[PositiveInt] = Field(min_length=2, max_length=64)