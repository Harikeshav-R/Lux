from typing import Type

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
    def __init__(self):
        self.client = G4FClient()
        self.conversations: list[Conversation] = []
        self.current_conversation: Conversation | None = None

    def start_new_conversation(self, system_prompt: str = settings.get("llm.default_system_prompt")):
        self.conversations.append(Conversation(system_prompt))
        self.current_conversation = self.conversations[-1]

    def generate_response(self, model: str, user_message: str, web_search: bool = False) -> str:
        if self.current_conversation is None:
            self.start_new_conversation()

        self.current_conversation.add_user_message(user_message)

        response = self.client.chat.completions.create(
            model=model,
            messages=self.current_conversation.get_conversation(),
            web_search=web_search
        )

        assistant_response = response.choices[0].message.content
        self.current_conversation.add_assistant_message(assistant_response)

        return assistant_response
