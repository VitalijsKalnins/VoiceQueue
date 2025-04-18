from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.database import mongo_connect, mongo_disconnect
from app.repository.profiles import profiles_repository

## API Routers
from app.api.v1.profiles import router as ProfilesRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Connect to mongo client
    await mongo_connect()
    yield
    ## Disconnect from mongo client
    await mongo_disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(ProfilesRouter, prefix="/v1", tags=["profiles"])