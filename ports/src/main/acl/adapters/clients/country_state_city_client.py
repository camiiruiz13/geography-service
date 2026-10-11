
import logging
import time
import httpx

from ports.src.main.acl.adapters.clients.dtos.config.country_state_city_config import CountryStateCityConfig
from ports.src.main.acl.adapters.clients.dtos.responses.country_dto import CountryDTO

logger = logging.getLogger(__name__)


class CountryStateCityClient:

    def __init__(self, config: CountryStateCityConfig):
        self.config = config

    async def get_countries(self) -> list[CountryDTO]:
        url = (f"{self.config.base_url.rstrip('/')}/"
            f"{self.config.endpoints.countries.lstrip('/')}")

        headers = {
            self.config.headers.api_key.key: self.config.headers.api_key.value,
            self.config.headers.accept.key: self.config.headers.accept.value,
        }

        start_time = time.perf_counter()

        logger.info("Starting Country State City countries request")

        try:
            async with httpx.AsyncClient(
                timeout=self.config.timeout
            ) as client:
                response = await client.get(
                    url,
                    headers=headers,
                )

                response.raise_for_status()

                countries = [
                    CountryDTO.model_validate(country)
                    for country in response.json()
                ]

                logger.info(
                    "Countries retrieved successfully. count=%s duration_ms=%.2f",
                    len(countries),
                    (time.perf_counter() - start_time) * 1000,
                )

                return countries

        except httpx.TimeoutException:
            logger.error(
                "Country State City request timeout. duration_ms=%.2f",
                (time.perf_counter() - start_time) * 1000,
            )
            raise

        except httpx.HTTPStatusError as exc:
            logger.error(
                "Country State City HTTP error. status_code=%s duration_ms=%.2f",
                exc.response.status_code,
                (time.perf_counter() - start_time) * 1000,
            )
            raise

        except httpx.RequestError as exc:
            logger.error(
                "Country State City connection error. type=%s duration_ms=%.2f",
                type(exc).__name__,
                (time.perf_counter() - start_time) * 1000,
            )
            raise
