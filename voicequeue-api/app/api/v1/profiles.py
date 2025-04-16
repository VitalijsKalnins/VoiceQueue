from fastapi import APIRouter
from app.service.profiles import service as ProfilesService
import app.schema.profiles as profiles_schema

## ProfilesRouter Declaration
router = APIRouter()

## GET v1/profiles/{profile_id}
@router.get("/profiles/{profile_id}", response_model=profiles_schema.GetProfileResponse)
async def get_profile(profile_id: int) -> profiles_schema.GetProfileResponse:
    ## Call Profiles Service for Profile
    profile = ProfilesService.GetProfile(profile_id=profile_id)

    return profile