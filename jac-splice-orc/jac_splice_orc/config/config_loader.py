# config_loader.py

import os
import json
import logging


class ConfigLoader:
    """Loads configurations from a JSON file."""

    def __init__(self, config_file_path=None):
        if config_file_path is None:
            # Default config file path
            config_file_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.config_file_path = config_file_path
        self.config = self.load_config()

        if module_config_path := os.getenv("MODULE_CONFIG_PATH", "/cfg/config.json"):
            try:
                logging.info(f"Loading from {module_config_path} for module_config...")
                with open(module_config_path, "r") as f:
                    self.config["module_config"] = json.load(f)
            except Exception as e:
                logging.warning(
                    f"No module_config found in config_map ({module_config_path}). "
                    f"Defaulting to fallback file. Error: {e}"
                )

    def load_config(self):
        """Load the JSON configuration file."""
        try:
            with open(self.config_file_path, "r") as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            logging.error(f"Configuration file not found at {self.config_file_path}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON configuration: {e}")
            raise

    def get(self, *keys, default=None):
        """Retrieve a configuration value using a sequence of keys."""
        cfg = self.config
        for key in keys:
            if cfg and key in cfg:
                cfg = cfg.get(key)
            else:
                return default
        return cfg if cfg is not None else default

    def set(self, keys, value):
        """Set a configuration value using a list of keys."""
        cfg = self.config
        for key in keys[:-1]:
            if key not in cfg or not isinstance(cfg[key], dict):
                cfg[key] = {}
            cfg = cfg[key]
        cfg[keys[-1]] = value

    def save_config(self):
        """Save the current configuration back to the JSON file."""
        try:
            with open(self.config_file_path, "w") as f:
                json.dump(self.config, f, indent=4)
            logging.info(f"Configuration saved to {self.config_file_path}")
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")
            raise
