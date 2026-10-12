
class ProviderErrorConstants:

    ERROR_MAPPING = {
        401: ("GEO_001", "PROVIDER_UNAUTHORIZED",
              "Country State City authentication failed", 502),
        403: ("GEO_002", "PROVIDER_FORBIDDEN",
              "Country State City access denied", 502),
        429: ("GEO_003", "PROVIDER_RATE_LIMIT",
              "Country State City request limit exceeded", 503),
    }

    DEFAULT_ERROR = (
        "GEO_005",
        "PROVIDER_ERROR",
        "Country State City request failed",
        502,
    )

    SERVER_ERROR = (
        "GEO_004",
        "PROVIDER_UNAVAILABLE",
        "Country State City service unavailable",
        502,
    )
