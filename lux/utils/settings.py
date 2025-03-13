import json
import os

from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_SETTINGS = {
    "database": {
        "url": "sqlite:///lux.db",
    }
}


class Settings:
    """
    A class to handle JSON-based settings management, allowing reading, writing,
    and modifying settings stored in a JSON file.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the Settings handler with a specified JSON file path.

        :param file_path: str - Path to the JSON settings file.
        :return: None
        """

        self.file_path: Path = Path(file_path)
        self.settings: Dict[str, Any] = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        """
        Loads settings from the JSON file. Returns an empty dictionary if the file does not exist or is invalid.

        :return: Dict[str, Any] - Dictionary containing the settings.
        """

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(DEFAULT_SETTINGS, file, indent=4)

            return DEFAULT_SETTINGS
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return DEFAULT_SETTINGS

    def _save_settings(self) -> None:
        """
        Saves the current settings to the JSON file.

        :return: None
        """

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.settings, file, indent=4)

    def _get_nested(self, keys: list[str], create_missing: bool = False) -> Optional[Dict[str, Any]]:
        """
        Retrieves a nested dictionary based on a list of keys. Optionally creates missing keys as empty dictionaries.

        :param keys: list[str] - List of keys representing the nested structure.
        :param create_missing: bool - If True, missing keys will be created.
        :return: Optional[Dict[str, Any]] - The nested dictionary or None if not found.
        """

        data: Dict[str, Any] = self.settings
        for key in keys[:-1]:
            if key not in data:
                if create_missing:
                    data[key] = {}
                else:
                    return None
            data = data[key]
        return data

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves the value for a given key. Supports nested keys using dot notation.

        :param key: str - Key string, supporting dot notation for nested values.
        :param default: Any - Default value to return if the key is not found.
        :return: Any - The value associated with the key or the default value.
        """

        keys: list[str] = key.split('.')
        data: Optional[Dict[str, Any]] = self._get_nested(keys)
        return data.get(keys[-1], default) if data else default

    def set(self, key: str, value: Any) -> None:
        """
        Sets a value for a given key. Supports nested keys using dot notation.

        :param key: str - Key string, supporting dot notation for nested values.
        :param value: Any - The value to set.
        :return: None
        """

        keys: list[str] = key.split('.')
        data: Optional[Dict[str, Any]] = self._get_nested(keys, create_missing=True)
        if data is not None:
            data[keys[-1]] = value
            self._save_settings()

    def remove(self, key: str) -> None:
        """
        Removes a key from the settings. Supports nested keys using dot notation.

        :param key: str - Key string, supporting dot notation for nested values.
        :return: None
        """

        keys: list[str] = key.split('.')
        data: Optional[Dict[str, Any]] = self._get_nested(keys)
        if data and keys[-1] in data:
            del data[keys[-1]]
            self._save_settings()

    def reset(self) -> None:
        """
        Resets all settings to an empty dictionary and saves the changes.

        :return: None
        """

        self.settings = {}
        self._save_settings()

    def get_all(self) -> Dict[str, Any]:
        """
        Returns a copy of all current settings.

        :return: Dict[str, Any] - A dictionary containing all settings.
        """

        return self.settings.copy()

    def update(self, new_settings: Dict[str, Any]) -> None:
        """
        Updates multiple settings at once by merging with existing settings.

        :param new_settings: Dict[str, Any] - Dictionary containing new settings to merge.
        :return: None
        """

        self.settings.update(new_settings)
        self._save_settings()


settings = Settings('lux-settings.json')
