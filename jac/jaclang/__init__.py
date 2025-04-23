"""The Jac Programming Language."""

from jaclang.runtimelib.feature import JacFeature, JacFeatureImpl, plugin_manager


plugin_manager.register(JacFeatureImpl)
plugin_manager.load_setuptools_entrypoints("jac")

__all__ = ["JacFeature"]
