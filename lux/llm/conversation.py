from typing import Any


class Conversation:
    def __init__(self, system_prompt: str):
        self._history: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

    def add_user_message(self, message: str, image_data: str | None = None) -> None:
        self._history.append(
            {
                "role": "user",
                "content": message,
                "image_data": image_data,
            }
        )

    def add_assistant_message(self, message: str, image_data: str | None = None) -> None:
        self._history.append(
            {
                "role": "assistant",
                "content": message,
                "image_data": image_data,
            }
        )

    def get_system_prompt(self) -> str:
        return self._history[0]["content"]

    def get_conversation(self) -> list[dict[str, Any]]:
        return self._history
