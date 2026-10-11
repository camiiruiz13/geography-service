
from unittest.mock import AsyncMock

import pytest

from core.src.main.application.environment import Environment
from core.src.main.domain.commands.country_commands import CountryCommands

from core.src.main.domain.models.country import Country
from core.src.main.domain.services.country_service import CountryService


class TestCountryCommands:

    @pytest.fixture
    def country_service(self):
        return AsyncMock(spec=CountryService)

    @pytest.fixture
    def commands(self, country_service):
        return CountryCommands(country_service)

    @pytest.fixture
    def country(self):
        return Country(
            idPais="48",
            nombre="Colombia",
            codigoIso2="CO",
            codigoIso3="COL",
            capital="Bogota",
            moneda="COP",
            indicativoTelefonico="57",
            emoji="🇨🇴",
        )

    def test_implements_environment(self, commands):
        assert isinstance(commands, Environment)

    @pytest.mark.asyncio
    async def test_get_countries_success(
        self,
        commands,
        country_service,
        country,
    ):
        country_service.get_countries.return_value = [country]

        result = await commands.get_countries()

        assert len(result) == 1
        assert isinstance(result[0], Country)
        assert result[0].idPais == "48"
        assert result[0].nombre == "Colombia"

        country_service.get_countries.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_get_countries_empty(
        self,
        commands,
        country_service,
    ):
        country_service.get_countries.return_value = []

        result = await commands.get_countries()

        assert result == []
        country_service.get_countries.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_get_countries_error(
        self,
        commands,
        country_service,
    ):
        country_service.get_countries.side_effect = ConnectionError(
            "Provider unavailable"
        )

        with pytest.raises(
            ConnectionError,
            match="Provider unavailable",
        ):
            await commands.get_countries()

        country_service.get_countries.assert_awaited_once_with()
