
from core.src.main.domain.models.country import Country
from ports.src.main.acl.adapters.clients.dtos.responses.country_dto import CountryDTO
from ports.src.main.acl.adapters.clients.transformer.country_transformer import CountryTransformer


class TestCountryTransformer:

    def test_to_domain(self):
        country_dto = CountryDTO(
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

        result = CountryTransformer.to_domain(country_dto)

        assert isinstance(result, Country)
        assert result.idPais == "48"
        assert result.nombre == "Colombia"
        assert result.codigoIso2 == "CO"
        assert result.codigoIso3 == "COL"
        assert result.capital == "Bogota"
        assert result.moneda == "COP"
        assert result.indicativoTelefonico == "57"
        assert result.emoji == "🇨🇴"
