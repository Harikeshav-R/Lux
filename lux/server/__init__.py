from fastapi import FastAPI

from lux.server.api import api_router
from lux.server.core.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)
