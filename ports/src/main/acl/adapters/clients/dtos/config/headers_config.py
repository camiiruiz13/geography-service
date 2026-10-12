from pydantic import BaseModel, Field

from ports.src.main.acl.adapters.clients.dtos.config.header_config import HeaderConfig
from ports.src.main.acl.constants.constants import ConfigConstants


class HeadersConfig(BaseModel):

    api_key: HeaderConfig = Field(alias=ConfigConstants.API_KEY_ALIAS)
    accept: HeaderConfig
