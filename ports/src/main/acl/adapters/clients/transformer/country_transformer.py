from core.src.main.domain.models.country import Country
from ports.src.main.acl.adapters.clients.dtos.responses.country_dto import CountryDTO


class CountryTransformer:

    @staticmethod
    def to_domain(country_dto: CountryDTO) -> Country:
        return Country(
            idPais=country_dto.id,
            nombre=country_dto.name,
            codigoIso2=country_dto.iso2,
            codigoIso3=country_dto.iso3,
            capital=country_dto.capital,
            moneda=country_dto.currency,
            indicativoTelefonico=country_dto.phonecode,
            emoji=country_dto.emoji,
        )
