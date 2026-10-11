
from pydantic import BaseModel, ConfigDict, Field

from ports.src.main.api.constants.api_constants import ApiConstants


class ErrorResponseDTO(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    code: str = Field(
        description="Código interno del error.",
        examples=[ApiConstants.PROVIDER_ERROR_CODE],
    )

    error: str = Field(
        description="Tipo de error.",
        examples=[ApiConstants.BAD_GATEWAY_ERROR],
    )

    message: str = Field(
        description="Descripción del error.",
        examples=[ApiConstants.PROVIDER_ERROR_MESSAGE],
    )
