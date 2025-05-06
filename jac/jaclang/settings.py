"""Main settings of jac lang."""

import configparser
import os
from dataclasses import dataclass, fields


@dataclass
class Settings:
    """Main settings of Jac lang."""

    # Debug configuration
    filter_sym_builtins: bool = True
    ast_symbol_info_detailed: bool = False
    pass_timer: bool = False
    collect_py_dep_debug: bool = False
    print_py_raised_ast: bool = False

    # Compiler configuration
    disable_mtllm: bool = False
    ignore_test_annex: bool = False
    pyout_jaclib_alias: str = "_"

    # Formatter configuration
    max_line_length: int = 88

    # LSP configuration
    lsp_debug: bool = False

    def __post_init__(self) -> None:
        """Initialize settings."""
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".jaclang")
        self.config_file_path = os.path.join(config_dir, "config.ini")
        os.makedirs(config_dir, exist_ok=True)
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, "w") as f:
                f.write("[settings]\n")
        self.load_all()

    def load_all(self) -> None:
        """Load settings from all available sources."""
        self.load_config_file()
        self.load_env_vars()

    def load_config_file(self) -> None:
        """Load settings from a configuration file."""
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_file_path)
        if "settings" in config_parser:
            for key in config_parser["settings"]:
                if key in [f.name for f in fields(self)]:
                    setattr(
                        self, key, self.convert_type(config_parser["settings"][key])
                    )

    def load_env_vars(self) -> None:
        """Override settings from environment variables if available."""
        for key in [f.name for f in fields(self)]:
            env_value = os.getenv("JACLANG_" + key.upper())
            env_value = (
                env_value if env_value is not None else os.getenv("JAC_" + key.upper())
            )
            if env_value is not None:
                setattr(self, key, self.convert_type(env_value))

        # def load_command_line_arguments(self):
        #     """Override settings from command-line arguments if provided."""
        #     parser = argparse.ArgumentParser()
        #     parser.add_argument(
        #         "--debug",
        #         type=self.str_to_bool,
        #         nargs="?",
        #         const=True,
        #         default=self.config["debug"],
        #     )
        #     parser.add_argument("--port", type=int, default=self.config["port"])
        #     parser.add_argument("--host", default=self.config["host"])
        #     args = parser.parse_args()

    def str_to_bool(self, value: str) -> bool:
        """Convert string to boolean."""
        return value.lower() in ("yes", "y", "true", "t", "1")

    def convert_type(self, value: str) -> bool | str | int:
        """Convert string values from the config to the appropriate type."""
        if value.isdigit():
            return int(value)
        if value.lower() in (
            "true",
            "false",
            "t",
            "f",
            "yes",
            "no",
            "y",
            "n",
            "1",
            "0",
        ):
            return self.str_to_bool(value)
        return value

    def __str__(self) -> str:
        """Return string representation of the settings."""
        return "\n".join(
            [f"{field.name}: {getattr(self, field.name)}" for field in fields(self)]
        )


settings = Settings()

__all__ = ["settings"]
