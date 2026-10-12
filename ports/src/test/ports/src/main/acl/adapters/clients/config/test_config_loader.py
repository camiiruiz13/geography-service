
import pytest

from ports.src.main.acl.adapters.clients.dtos.config.config_loader import ConfigLoader


class TestConfigLoader:

    def test_load_yaml_with_environment_variables(
        self,
        tmp_path,
        monkeypatch,
    ):
        monkeypatch.setenv(
            "CSC_BASE_URL",
            "https://api.example.com/v1",
        )
        monkeypatch.setenv(
            "CSC_API_KEY",
            "test-api-key",
        )

        config_file = tmp_path / "application.yaml"
        config_file.write_text(
            """
geography:
  providers:
    country-state-city:
      base-url: "${CSC_BASE_URL}"
      headers:
        api-key:
          key: "X-CSCAPI-KEY"
          value: "${CSC_API_KEY}"
      timeout: 10
      retries: 0
""",
            encoding="utf-8",
        )

        result = ConfigLoader(config_file).load()

        provider = result["geography"]["providers"]["country-state-city"]

        assert provider["base-url"] == "https://api.example.com/v1"
        assert provider["headers"]["api-key"]["value"] == "test-api-key"
        assert provider["timeout"] == 10
        assert provider["retries"] == 0

    def test_missing_environment_variable(
        self,
        tmp_path,
        monkeypatch,
    ):
        monkeypatch.delenv("CSC_MISSING_TEST_VARIABLE", raising=False)

        config_file = tmp_path / "application.yaml"
        config_file.write_text(
            'base-url: "${CSC_MISSING_TEST_VARIABLE}"',
            encoding="utf-8",
        )

        with pytest.raises(
            ValueError,
            match="Missing environment variable: CSC_MISSING_TEST_VARIABLE",
        ):
            ConfigLoader(config_file).load()

    def test_load_yaml_without_variables(
        self,
        tmp_path,
    ):
        config_file = tmp_path / "application.yaml"
        config_file.write_text(
            "timeout: 10\nretries: 0",
            encoding="utf-8",
        )

        result = ConfigLoader(config_file).load()

        assert result == {
            "timeout": 10,
            "retries": 0,
        }
