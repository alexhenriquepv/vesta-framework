from typing import Dict, Any

import yaml

from resources.logger import log, LogCategory


def load_config() -> Dict[str, Any]:
        try:
            with open('resources/config.yaml', 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError) as e:
            log(f"Error loading config.yaml: {e}. Exiting.", LogCategory.END)
            raise SystemExit from e