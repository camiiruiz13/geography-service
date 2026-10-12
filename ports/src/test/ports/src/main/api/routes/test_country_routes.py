
from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.src.main.application.environment import Environment
from core.src.main.domain.models.country import Country
from ports.src.main.api.constants.api_constants import ApiConstants
from ports.src.main.api.routes.country_routes import CountryRoutes


class TestCountryRoutes:

    @pytest.fixture
    def env(self):
        return AsyncMock(spec=Environment)

    @pytest.fixture
    def client(self, env):
        app = FastAPI()
        country_routes = CountryRoutes(env)
        app.include_router(country_routes.router)

        return TestClient(app)

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

    def test_get_countries_success(
        self,
        client,
        env,
        country,
    ):
        env.get_countries.return_value = [country]

        response = client.get(ApiConstants.COUNTRIES_ROUTE)

        assert response.status_code == ApiConstants.HTTP_OK

        body = response.json()

        assert body["data"] == [
            {
                "idPais": "48",
                "nombre": "Colombia",
                "codigoIso2": "CO",
                "codigoIso3": "COL",
                "capital": "Bogota",
                "moneda": "COP",
                "indicativoTelefonico": "57",
                "emoji": "🇨🇴",
            }
        ]

        assert body["pagination"] == {
            "page": 1,
            "pageSize": 20,
            "totalElements": 1,
            "totalPages": 1,
            "hasNext": False,
            "hasPrevious": False,
        }

        env.get_countries.assert_awaited_once_with()

    def test_get_countries_empty_response(
        self,
        client,
        env,
    ):
        env.get_countries.return_value = []

        response = client.get(ApiConstants.COUNTRIES_ROUTE)

        assert response.status_code == ApiConstants.HTTP_OK

        body = response.json()

        assert body["data"] == []
        assert body["pagination"] == {
            "page": 1,
            "pageSize": 20,
            "totalElements": 0,
            "totalPages": 0,
            "hasNext": False,
            "hasPrevious": False,
        }

        env.get_countries.assert_awaited_once_with()

    def test_get_countries_timeout(
        self,
        client,
        env,
    ):
        env.get_countries.side_effect = httpx.TimeoutException(
            "Provider timeout"
        )

        response = client.get(ApiConstants.COUNTRIES_ROUTE)

        assert (
            response.status_code
            == ApiConstants.HTTP_SERVICE_UNAVAILABLE
        )
        assert response.json() == {
            "code": ApiConstants.SERVICE_UNAVAILABLE_CODE,
            "error": ApiConstants.SERVICE_UNAVAILABLE_ERROR,
            "message": ApiConstants.SERVICE_UNAVAILABLE_MESSAGE,
        }

        env.get_countries.assert_awaited_once_with()

    def test_get_countries_connection_error(
        self,
        client,
        env,
    ):
        env.get_countries.side_effect = httpx.ConnectError(
            "Connection failed"
        )

        response = client.get(ApiConstants.COUNTRIES_ROUTE)

        assert response.status_code == ApiConstants.HTTP_BAD_GATEWAY
        assert response.json() == {
            "code": ApiConstants.PROVIDER_ERROR_CODE,
            "error": ApiConstants.BAD_GATEWAY_ERROR,
            "message": ApiConstants.PROVIDER_ERROR_MESSAGE,
        }

        env.get_countries.assert_awaited_once_with()

    def test_get_countries_http_error(
        self,
        client,
        env,
    ):
        request = httpx.Request(
            "GET",
            "https://example.com/countries",
        )

        provider_response = httpx.Response(
            status_code=500,
            request=request,
        )

        env.get_countries.side_effect = httpx.HTTPStatusError(
            "Provider returned HTTP 500",
            request=request,
            response=provider_response,
        )

        response = client.get(ApiConstants.COUNTRIES_ROUTE)

        assert response.status_code == ApiConstants.HTTP_BAD_GATEWAY
        assert response.json() == {
            "code": ApiConstants.PROVIDER_ERROR_CODE,
            "error": ApiConstants.BAD_GATEWAY_ERROR,
            "message": ApiConstants.PROVIDER_ERROR_MESSAGE,
        }

        env.get_countries.assert_awaited_once_with()

    def test_get_countries_swagger(
        self,
        client,
    ):
        response = client.get("/openapi.json")

        assert response.status_code == ApiConstants.HTTP_OK

        endpoint = response.json()["paths"][
            ApiConstants.COUNTRIES_ROUTE
        ]["get"]

        assert str(ApiConstants.HTTP_OK) in endpoint["responses"]
        assert str(ApiConstants.HTTP_BAD_GATEWAY) in endpoint["responses"]
        assert str(ApiConstants.HTTP_SERVICE_UNAVAILABLE) in endpoint["responses"]
