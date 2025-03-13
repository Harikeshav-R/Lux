from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from lux.server.core.db import get_db

from lux.server.crud.model import (
    read_all_models
)

from lux.server.schemas import LlmModelSchema

router = APIRouter()


@router.get("/", response_model=LlmModelSchema)
def read_all_models_endpoint(*, db: Session = Depends(get_db)):
    return read_all_models(db)
