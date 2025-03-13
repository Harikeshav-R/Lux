from lux.server.models.model import Model as LlmModelModel
from lux.server.schemas.model import Model as LlmModelSchema

import g4f
import g4f.models
import g4f.Provider

from sqlalchemy.orm import Session


def populate_models_in_database(db: Session):
    all_models = [LlmModelModel(
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


def read_all_models(db: Session):
    if not db.query(LlmModelModel).first():
        populate_models_in_database(db)

    return db.query(LlmModelModel).all()
