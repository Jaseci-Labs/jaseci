"""Jaclang setup file."""
from __future__ import annotations

from setuptools import find_packages, setup  # type: ignore


VERSION = "0.4.6"

setup(
    name="jaclang",
    version=VERSION,
    packages=find_packages(include=["jaclang", "jaclang.*"]),
    install_requires=[],
    package_data={
        "": ["*.ini"],
    },
    entry_points={
        "console_scripts": [
            "jac = jaclang.cli.cli:start_cli",
        ],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaclang",
)
