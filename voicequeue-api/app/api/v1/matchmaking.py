from fastapi import APIRouter, HTTPException
from app.service.matchmaking import service as MatchmakingService
from app.logging.logger import logger
import app.schema.matchmaking as Schema

## Matchmaking Router Declaration
router = APIRouter()

## GET /v1/matchmaking/
@router.get("/matchmaking/", response_model = Schema.GetMatchmakingResponse)
async def get_matchmaking(payload: Schema.GetMatchmakingRequest) -> Schema.GetMatchmakingResponse:
    matches = await MatchmakingService.matchmake(users=payload.ids)
    return Schema.GetMatchmakingResponse(matches=matches)