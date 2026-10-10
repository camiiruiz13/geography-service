import os
from pathlib import Path

from dotenv import load_dotenv


class EnvironmentConfig:

    def __init__(self, env_path: Path):
        load_dotenv(dotenv_path=env_path)

    def get(
        self,
        key: str,
        default: str | None = None,
    ) -> str:
        value = os.getenv(key, default)

        if value is None:
            raise ValueError(key)

        return value
