"""Jac Language Features."""

from typing import Any

from jaclang.plugin.default import hookimpl
from jaclang.plugin.feature import JacFeature as Jac


class JacPlugin:
    """Jaseci Implementations."""

    @staticmethod
    @hookimpl
    def report(expr: Any) -> None:  # noqa:ANN401
        """Jac's report stmt feature."""
        Jac.get_context().reports.append(expr)
