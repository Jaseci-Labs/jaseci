"""Formatter options for the prettier-style formatter.

This module contains the options for configuring the formatter behavior.
"""


class FormatterOptions:
    """Configuration options for the formatter."""

    def __init__(
        self,
        indent_size: int = 4,
        max_line_length: int = 80,
        tab_width: int = 4,
        use_tabs: bool = False,
        semicolons: bool = True,
        bracket_spacing: bool = True,
        trailing_comma: str = "all",
    ):
        """Initialize formatter options with defaults.

        Args:
            indent_size: Number of spaces per indentation level
            max_line_length: Maximum length of a line before wrapping
            tab_width: Width of a tab character
            use_tabs: Whether to use tabs for indentation
            semicolons: Whether to include semicolons
            bracket_spacing: Whether to add spaces between brackets
            trailing_comma: When to include trailing commas ("none", "es5", "all")
        """
        self.indent_size = indent_size
        self.max_line_length = max_line_length
        self.tab_width = tab_width
        self.use_tabs = use_tabs
        self.semicolons = semicolons
        self.bracket_spacing = bracket_spacing
        self.trailing_comma = trailing_comma

    @classmethod
    def from_config_file(cls, file_path: str) -> "FormatterOptions":
        """Load options from a configuration file.

        Args:
            file_path: Path to the configuration file

        Returns:
            FormatterOptions object with values from the config file
        """
        # TODO: Implement loading from config file
        return cls()

    def merge(self, overrides: "FormatterOptions") -> "FormatterOptions":
        """Create a new options object with the given overrides.

        Args:
            overrides: Options object with values to override

        Returns:
            New FormatterOptions object with merged values
        """
        new_options = self.__class__()
        for key, value in vars(self).items():
            setattr(new_options, key, getattr(overrides, key, value))
        return new_options
