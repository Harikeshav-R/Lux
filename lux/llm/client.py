import base64

from datetime import datetime
from pathlib import Path

import requests

from g4f import Client as G4FClient
from g4f.Provider import RetryProvider

from lux.llm.conversation import Conversation
from lux.llm.model import Model, TextModel, ImageModel, VisionModel
from lux.utils.settings import settings


class Client:
    def __init__(self, current_model: Model):
        self.current_model = current_model

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


class TextClient(Client):
    def __init__(self, model_name: str):
        super().__init__(TextModel(model_name))

    def generate_response(self, user_prompt: str, web_search: bool = False) -> None:
        if self._current_conversation is None:
            self.start_new_conversation()

        self._current_conversation.add_user_message(user_prompt)

        response = self._client.chat.completions.create(
            model=self.current_model.model_name,
            messages=self._current_conversation.get_conversation(),
            web_search=web_search,
        )

        assistant_response = response.choices[0].message.content
        self._current_conversation.add_assistant_message(assistant_response)


class ImageClient(Client):
    def __init__(self, model_name: str):
        super().__init__(ImageModel(model_name))

    def generate_response(self, user_prompt: str) -> None:
        if self._current_conversation is None:
            self.start_new_conversation()

        self._current_conversation.add_user_message(user_prompt)

        response = self._client.images.generate(
            model=self.current_model.model_name,
            prompt=user_prompt,
            response_format="b64_json"
        )

        generated_image = response.data[0].b64_json
        self._current_conversation.add_assistant_message("", generated_image)


class VisionClient(Client):
    def __init__(self, model_name: str):
        super().__init__(VisionModel(model_name))

    def generate_response(self, user_prompt: str, image_path: Path | None = None, web_search: bool = False) -> None:
        if self._current_conversation is None:
            self.start_new_conversation()

        if image_path is None:
            image_data = None

        else:
            with open(image_path, "rb") as f:
                image_data = f.read()

        self._current_conversation.add_user_message(user_prompt, base64.b64encode(image_data).decode(
            "utf-8") if image_data else None)

        response = self._client.chat.completions.create(
            model=self.current_model.model_name,
            messages=self._current_conversation.get_conversation(),
            web_search=web_search,
            image=image_data
        )

        assistant_response = response.choices[0].message.content
        self._current_conversation.add_assistant_message(assistant_response)
