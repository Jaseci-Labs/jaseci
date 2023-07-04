"""Jaclang setup file."""

from setuptools import find_packages, setup  # type: ignore

VERSION = "0.0.1"

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
            "jac = jaclang.cli:cli.run",
        ]
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaclang",
)
