
import logging
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest

from ports.src.main.acl.adapters.clients.country_state_city_client import (
    CountryStateCityClient,
)
from ports.src.main.acl.adapters.clients.dtos.config.config_bootstrap import (
    ConfigBootstrap,
)
from ports.src.main.acl.adapters.clients.dtos.config.country_state_city_config import (
    CountryStateCityConfig,
)
from ports.src.main.acl.constants.constants import ConfigConstants


class TestCountryStateCityClient:

    @pytest.fixture
    def config(self):
        test_src_path = Path(__file__).resolve().parents[3]

        bootstrap = ConfigBootstrap(
            config_path=(
                    test_src_path.parent
                    / "resources"
                    / "application.yml"
            ),
            env_path=test_src_path.parent / ".application",
        )

        provider = bootstrap.create_provider()

        return provider.get_config(
            section=(
                ConfigConstants.GEOGRAPHY_SECTION,
                ConfigConstants.PROVIDERS_SECTION,
                ConfigConstants.COUNTRY_STATE_CITY_SECTION,
            ),
            model=CountryStateCityConfig,
        )

    @pytest.fixture
    def countries_response(self):
        return [
            {
                "id": "48",
                "name": "Colombia",
                "iso2": "CO",
                "iso3": "COL",
                "phonecode": "57",
                "capital": "Bogota",
                "currency": "COP",
                "native": "Colombia",
                "region": "Americas",
                "region_id": None,
                "subregion": "South America",
                "subregion_id": None,
                "timezones": "[]",
                "latitude": "4.00000000",
                "longitude": "-72.00000000",
                "emoji": "🇨🇴",
            }
        ]

    async def execute_request(self, config, handler):
        transport = httpx.MockTransport(handler)

        real_async_client = httpx.AsyncClient

        def create_mock_client(*args, **kwargs):
            kwargs["transport"] = transport
            return real_async_client(*args, **kwargs)

        with patch(
            "ports.src.main.acl.adapters.clients."
            "country_state_city_client.httpx.AsyncClient",
            side_effect=create_mock_client,
        ):
            client = CountryStateCityClient(config)
            return await client.get_countries()

    @pytest.mark.asyncio
    async def test_get_countries_success(
        self,
        config,
        countries_response,
        caplog,
    ):
        def handler(request):
            assert request.url.path == "/countries"
            assert request.headers["X-CSCAPI-KEY"] == "test-secret-key"

            return httpx.Response(
                status_code=200,
                json=countries_response,
            )

        with caplog.at_level(logging.INFO):
            result = await self.execute_request(config, handler)

        assert len(result) == 1
        assert result[0].id == "48"
        assert result[0].name == "Colombia"
        assert result[0].iso2 == "CO"
        assert result[0].currency == "COP"

        assert "Countries retrieved successfully" in caplog.text
        assert "test-secret-key" not in caplog.text

    @pytest.mark.asyncio
    async def test_get_countries_empty_response(self, config):
        def handler(request):
            return httpx.Response(
                status_code=200,
                json=[],
            )

        result = await self.execute_request(config, handler)

        assert result == []

    @pytest.mark.asyncio
    async def test_get_countries_unauthorized(self, config, caplog):
        def handler(request):
            return httpx.Response(
                status_code=401,
                json={"message": "Unauthorized"},
            )

        with caplog.at_level(logging.ERROR):
            with pytest.raises(httpx.HTTPStatusError) as exc:
                await self.execute_request(config, handler)

        assert exc.value.response.status_code == 401
        assert "Country State City HTTP error" in caplog.text

    @pytest.mark.asyncio
    async def test_get_countries_server_error(self, config, caplog):
        def handler(request):
            return httpx.Response(
                status_code=500,
                json={"message": "Internal Server Error"},
            )

        with caplog.at_level(logging.ERROR):
            with pytest.raises(httpx.HTTPStatusError) as exc:
                await self.execute_request(config, handler)

        assert exc.value.response.status_code == 500
        assert "status_code=500" in caplog.text

    @pytest.mark.asyncio
    async def test_get_countries_timeout(self, config, caplog):
        def handler(request):
            raise httpx.ReadTimeout(
                "Request timed out",
                request=request,
            )

        with caplog.at_level(logging.ERROR):
            with pytest.raises(httpx.TimeoutException):
                await self.execute_request(config, handler)

        assert "Country State City request timeout" in caplog.text

    @pytest.mark.asyncio
    async def test_get_countries_connection_error(self, config, caplog):
        def handler(request):
            raise httpx.ConnectError(
                "Connection refused",
                request=request,
            )

        with caplog.at_level(logging.ERROR):
            with pytest.raises(httpx.RequestError):
                await self.execute_request(config, handler)

        assert "Country State City connection error" in caplog.text
