"""The Jac Programming Language."""

from jaclang.plugin.default import (  # noqa: E402
    JacBuiltin,
    JacCmdDefaults,
    JacFeatureDefaults,
)
from jaclang.plugin.feature import JacFeature, pm  # noqa: E402

jac_import = JacFeature.jac_import

pm.register(JacFeatureDefaults)
pm.register(JacBuiltin)
pm.register(JacCmdDefaults)
pm.load_setuptools_entrypoints("jac")

__all__ = ["jac_import"]
