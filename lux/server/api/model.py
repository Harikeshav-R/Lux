from fastapi import APIRouter, Depends, HTTPException
from g4f import ProviderType
from g4f.Provider import ProviderUtils
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

    # See different implementation in G4F API code
    if provider_name not in ProviderUtils.convert:
        raise HTTPException(status_code=404, detail="The given provider does not exist.")

    return read_model_by_provider(db, provider_name)