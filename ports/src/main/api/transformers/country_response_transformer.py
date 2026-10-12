
from core.src.main.domain.models.country import Country
from ports.src.main.api.dtos.responses.country_response_dto import CountryResponseDTO


class CountryResponseTransformer:

    @staticmethod
    def to_response(country: Country) -> CountryResponseDTO:
        return CountryResponseDTO(
            idPais=country.idPais,
            nombre=country.nombre,
            codigoIso2=country.codigoIso2,
            codigoIso3=country.codigoIso3,
            capital=country.capital,
            moneda=country.moneda,
            indicativoTelefonico=country.indicativoTelefonico,
            emoji=country.emoji,
        )
