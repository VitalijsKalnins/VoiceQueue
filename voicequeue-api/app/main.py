from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.database import mongo_connect, mongo_disconnect

@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Connect to mongo client
    await mongo_connect()
    yield
    ## Disconnect from mongo client
    await mongo_disconnect()

app = FastAPI(lifespan=lifespan)