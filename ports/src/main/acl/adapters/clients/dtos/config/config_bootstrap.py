
from pathlib import Path

from ports.src.main.acl.adapters.clients.dtos.config.config_loader import ConfigLoader
from ports.src.main.acl.adapters.clients.dtos.config.config_provider import ConfigProvider
from ports.src.main.acl.adapters.clients.dtos.config.environment_config import EnvironmentConfig
from ports.src.main.acl.adapters.clients.dtos.config.environment_resolver import EnvironmentResolver


class ConfigBootstrap:

    def __init__(
        self,
        config_path: Path,
        env_path: Path,
    ):
        self.config_path = config_path
        self.env_path = env_path

    def create_provider(self) -> ConfigProvider:
        environment = EnvironmentConfig(self.env_path)
        resolver = EnvironmentResolver(environment)
        loader = ConfigLoader(self.config_path)

        return ConfigProvider(loader, resolver)
