from typing import Type

from g4f import models
from g4f.providers.types import BaseProvider


class Model:
    all_models = \
        {
            str(model.name):
                {
                    "image": isinstance(model, models.ImageModel),
                    "vision": isinstance(model, models.VisionModel),
                    "providers":
                        [
                            (getattr(provider, "parent", provider.__name__), provider)
                            for provider in providers
                            if provider.working
                               and not provider.needs_auth
                               and not getattr(provider, "use_nodriver", False)
                        ]
                }
            for model, providers in models.__models__.values()
        }

    def __init__(self, model_name: str):
        self.model_name: str = model_name
        self.providers: dict[str, Type[BaseProvider]] = {
            provider_name: provider_class for provider_name, provider_class in self.all_models[model_name]["providers"]
        }


class TextModel(Model):
    all_models = {model: Model.all_models[model] for model in Model.all_models if not Model.all_models[model]["image"]}

    def __init__(self, model_name: str):
        if model_name not in self.all_models:
            raise ValueError(
                f"'{model_name}' is not a valid text model! Available models are: {', '.join(self.all_models.keys()).strip(', ')}")

        super().__init__(model_name)


class ImageModel(Model):
    all_models = {model: Model.all_models[model] for model in Model.all_models if Model.all_models[model]["image"]}

    def __init__(self, model_name: str):
        if model_name not in self.all_models:
            raise ValueError(
                f"'{model_name}' is not a valid image model! Available models are: {', '.join(self.all_models.keys()).strip(', ')}")

        super().__init__(model_name)


class VisionModel(Model):
    all_models = {model: Model.all_models[model] for model in Model.all_models if Model.all_models[model]["vision"]}

    def __init__(self, model_name: str):
        if model_name not in self.all_models:
            raise ValueError(
                f"'{model_name}' is not a valid vision model! Available models are: {', '.join(self.all_models.keys()).strip(', ')}")

        super().__init__(model_name)
