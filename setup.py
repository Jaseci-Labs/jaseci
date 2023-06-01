"""Jaseci setup file."""

from setuptools import find_packages, setup

VERSION = "2.0.0"

setup(
    name="jaseci",
    version=VERSION,
    packages=find_packages(include=["jaseci", "jaseci.*"]),
    install_requires=[
        "sly",
    ],
    package_data={
        "": ["*.ini"],
    },
    entry_points={
        # "console_scripts": [
        #     "jsctl = jaseci.cli_tools.jsctl:jsctl",
        #     "jac = jaseci.cli_tools.jsctl:jac",
        # ]
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci2",
)
