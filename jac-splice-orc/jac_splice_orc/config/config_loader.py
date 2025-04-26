import os
import json
import shutil
import logging


class ConfigLoader:
    """Loads and manages configurations from a JSON file."""

    def __init__(self, config_file_path=None):
        """Initialize the ConfigLoader."""
        # Figure out our default path
        self.default_config_file_path = os.path.join(
            os.path.dirname(__file__), "config.json"
        )
        # If user did not specify a path, use default
        if config_file_path is None:
            config_file_path = self.default_config_file_path

        self.default_config_file_path = self.default_config_file_path
        self.config_file_path = config_file_path
        self.config = self.load_config()

        # If user-specified path != default, copy the config over to default
        if config_file_path != self.default_config_file_path:
            self.copy_to_default()

    def load_config(self):
        """Load the JSON configuration file if it exists."""
        try:
            with open(self.config_file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file not found at {self.config_file_path}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON configuration: {e}")
            raise

    def copy_to_default(self):
        """Copy the loaded config into the default file path."""
        try:
            # Make sure the destination folder exists
            os.makedirs(os.path.dirname(self.default_config_file_path), exist_ok=True)
            shutil.copyfile(self.config_file_path, self.default_config_file_path)
            logging.info(
                f"Copied {self.config_file_path} => {self.default_config_file_path}"
            )
            # Update self.config_file_path to point to the default now
            self.config_file_path = self.default_config_file_path
        except Exception as e:
            logging.error(f"Failed to copy config to default location: {e}")

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
