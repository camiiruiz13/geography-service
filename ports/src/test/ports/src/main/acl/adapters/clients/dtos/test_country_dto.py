from ports.src.main.acl.adapters.clients.dtos.responses.country_dto import CountryDTO


class TestCountryDTO:

    def test_should_map_country_response(self):
        # Arrange
        response = {
            "id": "48",
            "name": "Colombia",
            "iso2": "CO",
            "iso3": "COL",
            "phonecode": "57",
            "capital": "Bogotá",
            "currency": "COP",
            "native": "Colombia",
            "region": "Americas",
            "region_id": "2",
            "subregion": "South America",
            "subregion_id": "8",
            "timezones": (
                '[{"zoneName": "America/Bogota", '
                '"gmtOffset": -18000, '
                '"gmtOffsetName": "UTC-05:00", '
                '"abbreviation": "COT", '
                '"tzName": "Colombia Time"}]'
            ),
            "latitude": "4",
            "longitude": "-72",
            "emoji": "🇨🇴"
        }

        # Act
        country = CountryDTO.model_validate(response)

        # Assert
        assert country.id == "48"
        assert country.name == "Colombia"
        assert country.iso2 == "CO"
        assert country.iso3 == "COL"
        assert country.phonecode == "57"
        assert country.capital == "Bogotá"
        assert country.currency == "COP"
        assert country.region == "Americas"
        assert country.latitude == "4"
        assert country.longitude == "-72"
        assert country.emoji == "🇨🇴"
