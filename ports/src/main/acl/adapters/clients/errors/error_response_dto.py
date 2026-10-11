
from pydantic import BaseModel

class ErrorResponseDTO(BaseModel):
    code: str
    error: str
    message: str
