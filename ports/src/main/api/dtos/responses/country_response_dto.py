
from pydantic import BaseModel, ConfigDict


class CountryResponseDTO(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "idPais": "48",
                "nombre": "Colombia",
                "codigoIso2": "CO",
                "codigoIso3": "COL",
                "capital": "Bogota",
                "moneda": "COP",
                "indicativoTelefonico": "57",
                "emoji": "🇨🇴",
            }
        },
    )

    idPais: str
    nombre: str
    codigoIso2: str
    codigoIso3: str
    capital: str
    moneda: str
    indicativoTelefonico: str
    emoji: str
