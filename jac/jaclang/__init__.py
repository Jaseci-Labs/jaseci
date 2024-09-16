"""The Jac Programming Language."""

from jaclang.plugin.default import JacFeatureImpl
from jaclang.plugin.feature import JacFeature, hookmanager

jac_import = JacFeature.jac_import


hookmanager.register(JacFeatureImpl)
hookmanager.load_setuptools_entrypoints("jac")

__all__ = ["jac_import"]
