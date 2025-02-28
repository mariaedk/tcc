"""
@author maria
date: 2025-02-26
"""
import json
import os

class MessageLoader:
    _messages = {}

    @classmethod
    def load_messages(cls, file_path: str = "app/config/strings.json"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo de mensagens não encontrado: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            cls._messages = json.load(f)

    @classmethod
    def get(cls, key: str, default: str = None):
        keys = key.split(".")
        data = cls._messages

        for k in keys:
            data = data.get(k)
            if data is None:
                return default

        return data

MessageLoader.load_messages()
