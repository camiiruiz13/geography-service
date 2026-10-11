import logging

import httpx
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from core.src.main.application.environment import Environment
from ports.src.main.acl.adapters.clients.dtos.responses.api_response_dto import ApiResponseDTO
from ports.src.main.api.constants.api_constants import ApiConstants
from ports.src.main.api.dtos.responses.country_response_dto import CountryResponseDTO
from ports.src.main.api.errors.ErrorResponseDTO import ErrorResponseDTO
from ports.src.main.api.transformers.api_response_transformer import (
    ApiResponseTransformer,
)
from ports.src.main.api.transformers.country_response_transformer import (
    CountryResponseTransformer,
)


logger = logging.getLogger(__name__)


class CountryRoutes:

    def __init__(self, env: Environment):
        self.env = env

        self.router = APIRouter(
            prefix=ApiConstants.COUNTRIES_ROUTE,
            tags=[ApiConstants.COUNTRIES_TAG],
        )

        self.router.add_api_route(
            path="",
            endpoint=self.get_countries,
            methods=["GET"],
            response_model=ApiResponseDTO[CountryResponseDTO],
            status_code=ApiConstants.HTTP_OK,
            summary=ApiConstants.GET_COUNTRIES_SUMMARY,
            description=ApiConstants.GET_COUNTRIES_DESCRIPTION,
            operation_id=ApiConstants.GET_COUNTRIES_OPERATION_ID,
            responses={
                ApiConstants.HTTP_BAD_GATEWAY: {
                    "model": ErrorResponseDTO,
                    "description": ApiConstants.BAD_GATEWAY_DESCRIPTION,
                },
                ApiConstants.HTTP_SERVICE_UNAVAILABLE: {
                    "model": ErrorResponseDTO,
                    "description": ApiConstants.SERVICE_UNAVAILABLE_DESCRIPTION,
                },
            },
        )

    async def get_countries(
        self,
        page: int = Query(
            default=1,
            ge=1,
            description="Número de página a consultar.",
        ),
        pageSize: int = Query(
            default=20,
            ge=1,
            le=100,
            description="Cantidad de países por página. Máximo 100.",
        ),
    ) -> ApiResponseDTO[CountryResponseDTO] | JSONResponse:

        try:
            countries = await self.env.get_countries()

            country_responses = [
                CountryResponseTransformer.to_response(country)
                for country in countries
            ]

            return ApiResponseTransformer.to_response(
                items=country_responses,
                page=page,
                page_size=pageSize,
            )

        except httpx.TimeoutException:
            logger.exception("Geographic provider timeout")

            error = ErrorResponseDTO(
                code=ApiConstants.SERVICE_UNAVAILABLE_CODE,
                error=ApiConstants.SERVICE_UNAVAILABLE_ERROR,
                message=ApiConstants.SERVICE_UNAVAILABLE_MESSAGE,
            )

            return JSONResponse(
                status_code=ApiConstants.HTTP_SERVICE_UNAVAILABLE,
                content=error.model_dump(),
            )

        except (httpx.RequestError, httpx.HTTPStatusError):
            logger.exception("Geographic provider request failed")

            error = ErrorResponseDTO(
                code=ApiConstants.PROVIDER_ERROR_CODE,
                error=ApiConstants.BAD_GATEWAY_ERROR,
                message=ApiConstants.PROVIDER_ERROR_MESSAGE,
            )

            return JSONResponse(
                status_code=ApiConstants.HTTP_BAD_GATEWAY,
                content=error.model_dump(),
            )