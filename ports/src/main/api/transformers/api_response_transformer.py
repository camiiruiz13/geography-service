from typing import TypeVar

from ports.src.main.acl.adapters.clients.dtos.responses.api_response_dto import ApiResponseDTO
from ports.src.main.api.util.paginator import Paginator

T = TypeVar("T")


class ApiResponseTransformer:

    @staticmethod
    def to_response(
        items: list[T],
        page: int,
        page_size: int,
    ) -> ApiResponseDTO[T]:

        return Paginator.paginate(
            items=items,
            page=page,
            page_size=page_size,
        )