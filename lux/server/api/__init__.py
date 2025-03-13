from fastapi import APIRouter

from lux.server.api import model

api_router = APIRouter(prefix="/api")
api_router.include_router(model.router, prefix="/model", tags=["model"])
