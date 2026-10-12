from pydantic import BaseModel, Field


class PaginationDTO(BaseModel):
    page: int = Field(ge=1)
    pageSize: int = Field(ge=1)
    totalElements: int = Field(ge=0)
    totalPages: int = Field(ge=0)
    hasNext: bool
    hasPrevious: bool