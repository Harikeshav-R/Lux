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

    return all_models


def read_all_models(db: Session) -> list[Model] | list[Type[Model]]:
    if not db.query(LlmModelModel).first():
        return _populate_models_in_database(db)

    return db.query(LlmModelModel).all()
