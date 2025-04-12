"""Core primitives for Jaseci."""

from jaclang.runtimelib.plugin.default import JacFeatureImpl
from jaclang.runtimelib.plugin.feature import plugin_manager

plugin_manager.register(JacFeatureImpl)
plugin_manager.load_setuptools_entrypoints("jac")
