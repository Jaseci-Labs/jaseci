"""The Jac Programming Language."""

from jaclang.runtimelib.default import JacFeatureImpl
from jaclang.runtimelib.feature import JacFeature, plugin_manager


plugin_manager.register(JacFeatureImpl)
plugin_manager.load_setuptools_entrypoints("jac")

__all__ = ["JacFeature"]
