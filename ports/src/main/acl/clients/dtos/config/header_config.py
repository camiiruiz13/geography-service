from pydantic import BaseModel

class HeaderConfig(BaseModel):
    key: str
    value: str