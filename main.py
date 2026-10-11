import logging
import os
from pathlib import Path
from fastapi import FastAPI

from core.src.main.domain.commands.country_commands import CountryCommands
from ports.src.main.acl.adapters.clients.country_state_city_client import CountryStateCityClient
from ports.src.main.acl.adapters.clients.dtos.config.config_loader import ConfigLoader
from ports.src.main.acl.adapters.clients.dtos.config.country_state_city_config import CountryStateCityConfig
from ports.src.main.acl.adapters.country_state_city_adapter import CountryStateCityAdapter
from ports.src.main.acl.constants.constants import ConfigConstants
from ports.src.main.api.constants.api_constants import ApiConstants
from ports.src.main.api.routes.country_routes import CountryRoutes


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    force=True,
)

app = FastAPI(
    title="Geography Service",
    description=(
        "API para consultar información geográfica "
        "de países, departamentos y municipios."
    ),
    version="1.0.0",
)

def configure_routes() -> None:
    config_path = (
            Path(__file__).resolve().parent
            / "ports"
            / "src"
            / "main"
            / "resources"
            / "application.yml"
    )

    config_data = ConfigLoader(config_path).load()

    provider_data = (
        config_data[ConfigConstants.GEOGRAPHY_SECTION]
        [ConfigConstants.PROVIDERS_SECTION]
        [ConfigConstants.COUNTRY_STATE_CITY_SECTION]
    )

    config = CountryStateCityConfig.model_validate(provider_data)

    client = CountryStateCityClient(config)
    adapter = CountryStateCityAdapter(client)
    commands = CountryCommands(adapter)

    country_routes = CountryRoutes(commands)

    app.include_router(
        country_routes.router,
        prefix=ApiConstants.API_PREFIX,
    )


configure_routes()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=int(os.getenv("PYTHON_PORT", "8000")),
        reload=True,
    )

