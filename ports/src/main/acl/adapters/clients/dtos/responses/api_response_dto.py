from typing import Generic, TypeVar

from pydantic import BaseModel

from ports.src.main.acl.adapters.clients.dtos.responses.pagination_dto import PaginationDTO

T = TypeVar("T")


class ApiResponseDTO(BaseModel, Generic[T]):
    data: list[T]
    pagination: PaginationDTO