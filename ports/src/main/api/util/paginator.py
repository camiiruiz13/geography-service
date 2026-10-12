from typing import TypeVar

from ports.src.main.acl.adapters.clients.dtos.responses.api_response_dto import ApiResponseDTO
from ports.src.main.acl.adapters.clients.dtos.responses.pagination_dto import PaginationDTO

T = TypeVar("T")


class Paginator:

    @staticmethod
    def paginate(
        items: list[T],
        page: int,
        page_size: int,
    ) -> ApiResponseDTO[T]:

        if page < 1:
            raise ValueError("Page must be greater than zero")

        if page_size < 1:
            raise ValueError("Page size must be greater than zero")

        total_elements = len(items)

        total_pages = (
            total_elements + page_size - 1
        ) // page_size

        start = (page - 1) * page_size
        end = start + page_size

        paginated_items = items[start:end]

        pagination = PaginationDTO(
            page=page,
            pageSize=page_size,
            totalElements=total_elements,
            totalPages=total_pages,
            hasNext=page < total_pages,
            hasPrevious=page > 1 and total_pages > 0,
        )

        return ApiResponseDTO[T](
            data=paginated_items,
            pagination=pagination,
        )