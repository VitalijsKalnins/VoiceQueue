from fastapi import APIRouter, HTTPException
from app.service.profiles import service as ProfilesService
from app.logging.logger import logger
import app.schema.profiles as Schema

## Profiles Router Declaration
router = APIRouter()

## GET /v1/profiles/{profile_id}
@router.get("/profiles/{profile_id}", response_model = Schema.GetProfileResponse)
async def get_profile(profile_id: int) -> Schema.GetProfileResponse:
    ## Call Profiles Service for Profile
    profile = await ProfilesService.get_profile(profile_id=profile_id)
    if profile is None: 
        raise HTTPException(status_code=404, detail="profile not found")
    return profile.to_response_dict()


## POST /v1/profiles/
@router.post("/profiles/", response_model = Schema.SetProfileResponse)
async def set_profile(payload: Schema.SetProfileRequest) -> Schema.SetProfileResponse:
    ok = await ProfilesService.set_profile(payload.id, payload.text)
    return Schema.SetProfileResponse(success=ok)