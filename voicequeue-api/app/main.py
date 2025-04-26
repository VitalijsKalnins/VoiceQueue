from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.database import mongo_connect, mongo_disconnect
from app.service.profiles import service as ProfilesService
from app.service.matchmaking import service as MatchmakingService
from app.service.nlp import service as NLPService
from app.logging.logger import logger

## API Routers
from app.api.v1.profiles import router as ProfilesRouter
from app.api.v1.matchmaking import router as MatchmakingRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Connect to mongo client
    await mongo_connect()
    yield
    ## Disconnect from mongo client
    await mongo_disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(ProfilesRouter, prefix="/v1", tags=["profiles"])
app.include_router(MatchmakingRouter, prefix="/v1", tags=["matchmaking"])