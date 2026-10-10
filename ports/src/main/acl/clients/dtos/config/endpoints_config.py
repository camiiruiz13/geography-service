from pydantic import BaseModel


class EndpointsConfig(BaseModel):

    countries: str
    states: str
    cities: str
