"""Jaseci setup file."""

from setuptools import find_packages, setup

VERSION = "2.0.0"

setup(
    name="jaseci",
    version=VERSION,
    packages=find_packages(include=["jaseci", "jaseci.*"]),
    install_requires=[
        "click>=8.1.0,<8.2.0",
        "click-shell>=2.1,<2.2",
        "flake8",
        "pep8-naming",
        "pytest",
        "pytest-xdist",
        "pytest-cov",
    ],
    package_data={
        "": ["*.ini"],
    },
    entry_points={
        "console_scripts": [
            "jsctl = jaseci.cli_tools.jsctl:jsctl",
            "jac = jaseci.cli_tools.jsctl:jac",
        ]
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci2",
)
