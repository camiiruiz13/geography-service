
class ApiConstants:

    # Routes
    API_PREFIX = "/boissonapp/geography"
    COUNTRIES_ROUTE = "/paises"
    COUNTRIES_TAG = "Countries"

    # Swagger - Countries
    GET_COUNTRIES_SUMMARY = "Consultar países"
    GET_COUNTRIES_DESCRIPTION = (
        "Obtiene el listado de países disponibles."
    )
    GET_COUNTRIES_OPERATION_ID = "getCountries"

    # HTTP status codes
    HTTP_OK = 200
    HTTP_BAD_GATEWAY = 502
    HTTP_SERVICE_UNAVAILABLE = 503

    # Swagger - Error descriptions
    BAD_GATEWAY_DESCRIPTION = (
        "Error de comunicación con el proveedor geográfico."
    )
    SERVICE_UNAVAILABLE_DESCRIPTION = (
        "Servicio geográfico no disponible."
    )

    # Error codes
    PROVIDER_ERROR_CODE = "PROVIDER_ERROR"
    SERVICE_UNAVAILABLE_CODE = "SERVICE_UNAVAILABLE"

    # Error names
    BAD_GATEWAY_ERROR = "Bad Gateway"
    SERVICE_UNAVAILABLE_ERROR = "Service Unavailable"

    # Error messages
    PROVIDER_ERROR_MESSAGE = (
        "No fue posible consultar el proveedor geográfico."
    )
    SERVICE_UNAVAILABLE_MESSAGE = (
        "El servicio geográfico no está disponible."
    )
