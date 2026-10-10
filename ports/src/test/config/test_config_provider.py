
from pathlib import Path

from ports.src.main.acl.clients.dtos.config.config_bootstrap import ConfigBootstrap
from ports.src.main.acl.clients.dtos.config.country_state_city_config import CountryStateCityConfig
from ports.src.main.acl.constants.constants import ConfigConstants


class TestConfigProvider:

    def test_load_country_state_city_config(self):
        project_root = Path(__file__).resolve().parents[4]

        bootstrap = ConfigBootstrap(
            config_path=(
                project_root
                / "ports/src/main/resources/application.yml"
            ),
            env_path=project_root / ".env",
        )

        provider = bootstrap.create_provider()

        config = provider.get_config(
            section=(
                ConfigConstants.GEOGRAPHY_SECTION,
                ConfigConstants.PROVIDERS_SECTION,
                ConfigConstants.COUNTRY_STATE_CITY_SECTION,
            ),
            model=CountryStateCityConfig,
        )

        assert isinstance(config, CountryStateCityConfig)
        assert config.base_url
        assert config.headers.api_key.value
        assert config.headers.accept.value
        assert config.endpoints.countries
        assert config.endpoints.states
        assert config.endpoints.cities
        assert config.timeout > 0
        assert config.retries >= 0
