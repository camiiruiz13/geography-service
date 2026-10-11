import os
import re
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from ports.src.main.acl.constants.constants import ConfigConstants


class ConfigLoader:

    def __init__(self, config_path: Path):
        self.config_path = config_path

    def load(self) -> dict[str, Any]:
        load_dotenv()

        with self.config_path.open(
            mode=ConfigConstants.READ_MODE,
            encoding=ConfigConstants.ENCODING,
        ) as file:
            config = yaml.safe_load(file)

        return self._resolve_variables(config)

    def _resolve_variables(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: self._resolve_variables(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                self._resolve_variables(item)
                for item in value
            ]

        if isinstance(value, str):
            return re.sub(
                ConfigConstants.ENV_VARIABLE_PATTERN,
                self._replace_env_variable,
                value,
            )

        return value

    @staticmethod
    def _replace_env_variable(match: re.Match[str]) -> str:
        variable = match.group(1)
        result = os.getenv(variable)

        if result is None:
            raise ValueError(
                ConfigConstants.MISSING_ENV_VARIABLE.format(variable)
            )

        return result