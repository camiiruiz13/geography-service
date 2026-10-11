
from unittest.mock import AsyncMock

import pytest

from core.src.main.domain.models.country import Country
from core.src.main.domain.services.country_service import CountryService
from ports.src.main.acl.adapters.clients.country_state_city_client import (
    CountryStateCityClient,
)
from ports.src.main.acl.adapters.clients.dtos.responses.country_dto import (
    CountryDTO,
)
from ports.src.main.acl.adapters.country_state_city_adapter import (
    CountryStateCityAdapter,
)


class TestCountryStateCityAdapter:

    @pytest.fixture
    def client(self):
        return AsyncMock(spec=CountryStateCityClient)

    @pytest.fixture
    def adapter(self, client):
        return CountryStateCityAdapter(client)

    @pytest.fixture
    def country_dto(self):
        return CountryDTO(
            id="48",
            name="Colombia",
            iso2="CO",
            iso3="COL",
            phonecode="57",
            capital="Bogota",
            currency="COP",
            native="Colombia",
            region="Americas",
            region_id=None,
            subregion="South America",
            subregion_id=None,
            timezones="[]",
            latitude="4.00000000",
            longitude="-72.00000000",
            emoji="🇨🇴",
        )

    def test_implements_country_service(self, adapter):
        assert isinstance(adapter, CountryService)

    @pytest.mark.asyncio
    async def test_get_countries_success(
        self,
        adapter,
        client,
        country_dto,
    ):
        client.get_countries.return_value = [country_dto]

        result = await adapter.get_countries()

        assert len(result) == 1
        assert isinstance(result[0], Country)
        assert result[0].idPais == "48"
        assert result[0].nombre == "Colombia"
        assert result[0].codigoIso2 == "CO"
        assert result[0].codigoIso3 == "COL"
        assert result[0].capital == "Bogota"
        assert result[0].moneda == "COP"
        assert result[0].indicativoTelefonico == "57"
        assert result[0].emoji == "🇨🇴"

        client.get_countries.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_get_countries_empty_response(
        self,
        adapter,
        client,
    ):
        client.get_countries.return_value = []

        result = await adapter.get_countries()

        assert result == []
        client.get_countries.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_get_countries_multiple(
        self,
        adapter,
        client,
        country_dto,
    ):
        second_country = country_dto.model_copy(
            update={
                "id": "49",
                "name": "Argentina",
                "iso2": "AR",
                "iso3": "ARG",
            }
        )

        client.get_countries.return_value = [
            country_dto,
            second_country,
        ]

        result = await adapter.get_countries()

        assert len(result) == 2

        assert result[0].idPais == "48"
        assert result[0].nombre == "Colombia"
        assert result[0].codigoIso2 == "CO"

        assert result[1].idPais == "49"
        assert result[1].nombre == "Argentina"
        assert result[1].codigoIso2 == "AR"
        assert result[1].codigoIso3 == "ARG"

        client.get_countries.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_get_countries_client_error(
        self,
        adapter,
        client,
    ):
        client.get_countries.side_effect = ConnectionError(
            "Provider unavailable"
        )

        with pytest.raises(
            ConnectionError,
            match="Provider unavailable",
        ):
            await adapter.get_countries()

        client.get_countries.assert_awaited_once_with()
