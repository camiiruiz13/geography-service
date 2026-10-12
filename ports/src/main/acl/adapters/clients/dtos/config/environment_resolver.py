
import re
from typing import Any
from ports.src.main.acl.adapters.clients.dtos.config.environment_config import EnvironmentConfig
from ports.src.main.acl.constants.constants import ConfigConstants

class EnvironmentResolver:

    def __init__(self, environment: EnvironmentConfig):
        self.environment = environment

    def resolve(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: self.resolve(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                self.resolve(item)
                for item in value
            ]

        if isinstance(value, str):
            return re.sub(
                ConfigConstants.ENV_VARIABLE_PATTERN,
                self._resolve_variable,
                value,
            )

        return value

    def _resolve_variable(self, match: re.Match[str]) -> str:
        variable_name = match.group(1)

        return self.environment.get(variable_name)
