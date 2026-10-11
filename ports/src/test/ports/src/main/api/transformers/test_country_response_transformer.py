
from core.src.main.domain.models.country import Country
from ports.src.main.api.dtos.responses.country_response_dto import CountryResponseDTO

from ports.src.main.api.transformers.country_response_transformer import (
    CountryResponseTransformer,
)


class TestCountryResponseTransformer:

    def test_to_response(self):
        country = Country(
            idPais="48",
            nombre="Colombia",
            codigoIso2="CO",
            codigoIso3="COL",
            capital="Bogota",
            moneda="COP",
            indicativoTelefonico="57",
            emoji="🇨🇴",
        )

        result = CountryResponseTransformer.to_response(country)

        assert isinstance(result, CountryResponseDTO)
        assert result.idPais == "48"
        assert result.nombre == "Colombia"
        assert result.codigoIso2 == "CO"
        assert result.codigoIso3 == "COL"
        assert result.capital == "Bogota"
        assert result.moneda == "COP"
        assert result.indicativoTelefonico == "57"
        assert result.emoji == "🇨🇴"

    def test_to_response_json(self):
        country = Country(
            idPais="48",
            nombre="Colombia",
            codigoIso2="CO",
            codigoIso3="COL",
            capital="Bogota",
            moneda="COP",
            indicativoTelefonico="57",
            emoji="🇨🇴",
        )

        result = CountryResponseTransformer.to_response(country)

        assert result.model_dump() == {
            "idPais": "48",
            "nombre": "Colombia",
            "codigoIso2": "CO",
            "codigoIso3": "COL",
            "capital": "Bogota",
            "moneda": "COP",
            "indicativoTelefonico": "57",
            "emoji": "🇨🇴",
        }
