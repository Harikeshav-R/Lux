from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from lux.server.core.db import get_db

from lux.server.crud.model import (
    read_all_models,
    read_model_by_provider
)

from lux.server.schemas import LlmModelSchema

router = APIRouter()


@router.get("/", response_model=list[LlmModelSchema])
def read_all_models_endpoint(*, db: Session = Depends(get_db), provider_name: str | None = None):
    if not provider_name:
        return read_all_models(db)

    return read_model_by_provider(db, provider_name)