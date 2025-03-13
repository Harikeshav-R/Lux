from typing import Type

from lux.server.models import LlmModelModel

import g4f
import g4f.models
import g4f.Provider

from sqlalchemy.orm import Session

from lux.server.models.model import Model


def _populate_models_in_database(db: Session) -> list[LlmModelModel]:
    all_models = [
                     LlmModelModel(
                         model_name=model_id,
                         base_provider=model.base_provider,
                         is_provider=False,
                         supports_image_generation=isinstance(model, g4f.models.ImageModel),
                     ) for model_id, model in
                     g4f.models.ModelUtils.convert.items()] + [
                     LlmModelModel(
                         model_name=provider_name,
                         base_provider=getattr(provider, "label", None),
                         is_provider=True,
                         supports_image_generation=bool(getattr(provider, "image_models", False))
                     ) for provider_name, provider in g4f.Provider.ProviderUtils.convert.items()
                     if provider.working and provider_name != "Custom"
                 ]

    db.add_all(all_models)
    db.commit()
    db.expire_all()


def read_all_models(db: Session) -> list[Model] | list[Type[Model]]:
    if not db.query(LlmModelModel).first():
        _populate_models_in_database(db)

    return db.query(LlmModelModel).all()


def read_model_by_provider(db: Session, provider_name: str) -> list[Model] | list[Type[Model]]:
    if not db.query(LlmModelModel).first():
        _populate_models_in_database(db)

    return db.query(LlmModelModel).filter(LlmModelModel.base_provider == provider_name).all()