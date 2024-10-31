"""The Jac Programming Language."""

from jaclang.plugin.default import JacFeatureImpl
from jaclang.plugin.feature import JacFeature, plugin_manager

jac_import = JacFeature.jac_import


plugin_manager.register(JacFeatureImpl)
plugin_manager.load_setuptools_entrypoints("jac")

__all__ = ["jac_import"]
