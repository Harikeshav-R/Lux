from g4f import Client as G4FClient

from lux.llm.conversation import Conversation
from lux.utils.settings import settings


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
