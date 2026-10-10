class ConfigConstants:

    ENCODING = "utf-8"
    READ_MODE = "r"

    GEOGRAPHY_SECTION = "geography"
    PROVIDERS_SECTION = "providers"
    COUNTRY_STATE_CITY_SECTION = "country-state-city"

    ENV_VARIABLE_PATTERN = r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"

    MISSING_ENV_VARIABLE = "Missing environment variable: {}"

    API_KEY_ALIAS = "api-key"
    BASE_URL_ALIAS = "base-url"
