import logging

from core.src.main.application.environment import Environment
from core.src.main.domain.models.country import Country
from core.src.main.domain.services.country_service import CountryService


logger = logging.getLogger(__name__)


class CountryCommands(Environment):

    def __init__(self, country_service: CountryService):
        self.country_service = country_service

    async def get_countries(self) -> list[Country]:
        logger.info("Executing get countries")

        countries = await self.country_service.get_countries()

        logger.info(
            "Countries retrieved successfully. Total: %s",
            len(countries),
        )

        return countries