
from typing import TypeVar

from pydantic import BaseModel

from ports.src.main.acl.adapters.clients.dtos.config.config_loader import ConfigLoader
from ports.src.main.acl.adapters.clients.dtos.config.environment_resolver import EnvironmentResolver

T = TypeVar("T", bound=BaseModel)


class ConfigProvider:

    def __init__(
        self,
        loader: ConfigLoader,
        resolver: EnvironmentResolver,
    ):
        self.loader = loader
        self.resolver = resolver

    def get_config(
        self,
        section: tuple[str, ...],
        model: type[T],
    ) -> T:
        config = self.loader.load()

        for key in section:
            config = config[key]

        resolved_config = self.resolver.resolve(config)

        return model.model_validate(resolved_config)
