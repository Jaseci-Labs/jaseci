"""The Jac Programming Language."""

from jaclang.plugin.default import (
    JacAccessValidation,
    JacBuiltin,
    JacCmdDefaults,
    JacFeatureDefaults,
    JacNode,
)
from jaclang.plugin.feature import JacFeature, hookmanager

jac_import = JacFeature.jac_import


hookmanager.register(JacFeatureDefaults)
hookmanager.register(JacBuiltin)
hookmanager.register(JacCmdDefaults)
hookmanager.register(JacAccessValidation)
hookmanager.register(JacNode)
hookmanager.load_setuptools_entrypoints("jac")

__all__ = ["jac_import"]
