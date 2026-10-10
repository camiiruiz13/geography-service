from pathlib import Path
from typing import Any

import yaml

from ports.src.main.acl.constants.constants import ConfigConstants


class ConfigLoader:

    def __init__(self, config_path: Path):
        self.config_path = config_path

    def load(self) -> dict[str, Any]:
        with self.config_path.open(mode=ConfigConstants.READ_MODE,
            encoding=ConfigConstants.ENCODING,) as file:
            return yaml.safe_load(file)