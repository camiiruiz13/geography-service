
from pydantic import BaseModel

class CountryDTO(BaseModel):
    id: str
    name: str
    iso2: str
    iso3: str
    phonecode: str
    capital: str
    currency: str
    native: str
    region: str
    region_id: str | None
    subregion: str
    subregion_id: str | None
    timezones: str
    latitude: str
    longitude: str
    emoji: str
