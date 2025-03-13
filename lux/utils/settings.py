import json
import os

from pathlib import Path
from typing import Any, Dict, Optional


class Settings:
    def __init__(self, file_path: str) -> None:
        self.file_path: Path = Path(file_path)
        self.settings: Dict[str, Any] = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def _save_settings(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.settings, file, indent=4)

    def _get_nested(self, keys: list[str], create_missing: bool = False) -> Optional[Dict[str, Any]]:
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
        keys: list[str] = key.split('.')
        data: Optional[Dict[str, Any]] = self._get_nested(keys)
        return data.get(keys[-1], default) if data else default

    def set(self, key: str, value: Any) -> None:
        keys: list[str] = key.split('.')
        data: Optional[Dict[str, Any]] = self._get_nested(keys, create_missing=True)
        if data is not None:
            data[keys[-1]] = value
            self._save_settings()

    def remove(self, key: str) -> None:
        keys: list[str] = key.split('.')
        data: Optional[Dict[str, Any]] = self._get_nested(keys)
        if data and keys[-1] in data:
            del data[keys[-1]]
            self._save_settings()

    def reset(self) -> None:
        self.settings = {}
        self._save_settings()

    def get_all(self) -> Dict[str, Any]:
        return self.settings.copy()

    def update(self, new_settings: Dict[str, Any]) -> None:
        self.settings.update(new_settings)
        self._save_settings()


settings = Settings('settings.json')