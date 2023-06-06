"""Jaclang setup file."""

from setuptools import find_packages, setup

VERSION = "2.0.0"

setup(
    name="jaclang",
    version=VERSION,
    packages=find_packages(include=["jaclang", "jaclang.*"]),
    install_requires=[],
    package_data={
        "": ["*.ini"],
    },
    entry_points={},
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci2",
)
