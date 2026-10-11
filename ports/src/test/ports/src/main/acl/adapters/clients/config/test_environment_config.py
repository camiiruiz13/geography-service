
from pathlib import Path

import pytest

from ports.src.main.acl.adapters.clients.dtos.config.environment_config import (
    EnvironmentConfig,
)


class TestEnvironmentConfig:

    def test_load_environment_secrets(self):
        project_root = Path(__file__).resolve().parents[4]

        environment = EnvironmentConfig(
            env_path=project_root / ".application"
        )

        base_url = environment.get("CSC_BASE_URL")
        api_key = environment.get("CSC_API_KEY")

        assert base_url.startswith("https://")
        assert api_key.strip()
        assert api_key.strip(), "CSC_API_KEY is missing or empty"

    def test_missing_required_secret(self, monkeypatch):
        project_root = Path(__file__).resolve().parents[4]

        environment = EnvironmentConfig(
            env_path=project_root / ".application"
        )

        monkeypatch.delenv(
            "GEOGRAPHY_TEST_MISSING_SECRET",
            raising=False,
        )

        with pytest.raises(ValueError):
            environment.get("GEOGRAPHY_TEST_MISSING_SECRET")
