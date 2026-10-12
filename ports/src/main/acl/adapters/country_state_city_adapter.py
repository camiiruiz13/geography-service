
import logging

from core.src.main.domain.models.country import Country
from core.src.main.domain.services.country_service import CountryService
from ports.src.main.acl.adapters.clients.country_state_city_client import CountryStateCityClient
from ports.src.main.acl.adapters.clients.transformer.country_transformer import CountryTransformer

logger = logging.getLogger(__name__)


class CountryStateCityAdapter(CountryService):

    def __init__(self, client: CountryStateCityClient):
        self.client = client

    async def get_countries(self) -> list[Country]:
        logger.info("Starting countries retrieval")

        countries_dto = await self.client.get_countries()

        countries = [CountryTransformer.to_domain(country_dto)
            for country_dto in countries_dto]

        logger.info( "Countries transformed successfully. count=%s",
            len(countries),)

        return countries
