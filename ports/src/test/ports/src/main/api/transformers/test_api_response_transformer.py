
from unittest.mock import patch

from ports.src.main.api.transformers.api_response_transformer import (
    ApiResponseTransformer,
)


class TestApiResponseTransformer:

    def test_to_response_success(self):
        items = ["Colombia", "Argentina", "Chile"]
        expected_response = object()

        with patch.object(
            ApiResponseTransformer.to_response.__globals__["Paginator"],
            "paginate",
            return_value=expected_response,
        ) as mock_paginate:
            result = ApiResponseTransformer.to_response(
                items=items,
                page=1,
                page_size=2,
            )

        mock_paginate.assert_called_once_with(
            items=items,
            page=1,
            page_size=2,
        )
        assert result is expected_response

    def test_to_response_empty_items(self):
        items = []
        expected_response = object()

        with patch.object(
            ApiResponseTransformer.to_response.__globals__["Paginator"],
            "paginate",
            return_value=expected_response,
        ) as mock_paginate:
            result = ApiResponseTransformer.to_response(
                items=items,
                page=1,
                page_size=20,
            )

        mock_paginate.assert_called_once_with(
            items=[],
            page=1,
            page_size=20,
        )
        assert result is expected_response
