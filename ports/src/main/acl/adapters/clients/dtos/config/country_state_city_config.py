from pydantic import BaseModel, Field

from ports.src.main.acl.adapters.clients.dtos.config.endpoints_config import EndpointsConfig
from ports.src.main.acl.adapters.clients.dtos.config.headers_config import HeadersConfig
from ports.src.main.acl.constants.constants import ConfigConstants


class CountryStateCityConfig(BaseModel):

    base_url: str = Field(alias=ConfigConstants.BASE_URL_ALIAS)

    headers: HeadersConfig
    endpoints: EndpointsConfig

    timeout: int = Field(gt=0)
    retries: int = Field(ge=0)
