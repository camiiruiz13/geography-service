from pydantic import BaseModel

class Country(BaseModel):
    idPais: str
    nombre: str
    codigoIso2: str
    codigoIso3: str
    capital: str
    moneda: str
    indicativoTelefonico: str
    emoji: str
