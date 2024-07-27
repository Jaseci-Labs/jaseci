"""Streamlit of Jac."""

from jac_streamlit.app_test import JacAppTest as AppTest


def run_streamlit(basename: str, dirname: str) -> None:
    """Run the Streamlit application."""
    from jaclang import jac_import
    from jaclang.plugin.feature import JacFeature as Jac

    Jac.context().init_memory(base_path=dirname)
    jac_import(basename, base_path=dirname)


__all__ = ["AppTest", "run_streamlit"]
