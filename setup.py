"""Jaclang setup file."""
from __future__ import annotations

from jaclang.cli import cli  # noqa: F401

from setuptools import find_packages, setup  # type: ignore


VERSION = "0.3.2"

setup(
    name="jaclang",
    version=VERSION,
    packages=find_packages(include=["jaclang", "jaclang.*"]),
    install_requires=[],
    package_data={
        "": ["*.ini", "*.jac"],
    },
    entry_points={
        "console_scripts": [
            "jac = jaclang.cli:cli.start_cli",
        ],
        "jac": ["corelib = jaclang.core:JacPlugin"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaclang",
)
