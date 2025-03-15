from datetime import datetime
from pathlib import Path
from typing import Type

import requests

from g4f import Client as G4FClient
from g4f import models
from g4f.Provider import RetryProvider
from g4f.providers.types import BaseProvider

from lux.llm.conversation import Conversation
from lux.utils.settings import settings


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
        if model_name not in self.all_models:
            raise ValueError(
                f"'{model_name}' is not a valid model! Available models are: {', '.join(self.all_models.keys()).strip(', ')}")

        self.model_name: str = model_name
        self.image_model: bool = self.all_models[model_name]["image"]
        self.vision_model: bool = self.all_models[model_name]["vision"]
        self.providers: dict[str, Type[BaseProvider]] = {
            provider_name: provider_class for provider_name, provider_class in self.all_models[model_name]["providers"]
        }


class Client:
    def __init__(self, model_name: str):
        self.current_model = Model(model_name)

        self._client = G4FClient(
            provider=RetryProvider(
                providers=list(self.current_model.providers.values()),
                shuffle=True,
            )
        )
        self._conversations: list[Conversation] = []
        self._current_conversation: Conversation | None = None

    def start_new_conversation(self, system_prompt: str = settings.get("llm.default_system_prompt")):
        self._conversations.append(Conversation(system_prompt))
        self._current_conversation = self._conversations[-1]

    def generate_text_response(self, web_search: bool = False) -> str:
        response = self._client.chat.completions.create(
            model=self.current_model.model_name,
            messages=self._current_conversation.get_conversation(),
            web_search=web_search
        )

        assistant_response = response.choices[0].message.content
        return assistant_response

    def generate_image_response(self) -> str:
        response = self._client.images.generate(
            model=self.current_model.model_name,
            prompt=self._current_conversation.get_conversation()[-1]["content"],
            response_format="url"
        )

        image_url = response.data[0].url

        response = requests.get(image_url)
        _, extension = response.headers["content-type"].split("/")
        file_name = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.{extension}"
        file_path = Path(settings.get("llm.images_location"), file_name)

        with open(file_path, "wb") as f:
            f.write(response.content)

        return str(file_path)

    def generate_response(self, user_message: str) -> str:
        if self._current_conversation is None:
            self.start_new_conversation()

        self._current_conversation.add_user_message(user_message)

        if self.current_model.image_model:
            assistant_response = self.generate_image_response()

        else:
            assistant_response = self.generate_text_response()

        self._current_conversation.add_assistant_message(assistant_response)
        return assistant_response
