"""Jaclang setup file."""

from setuptools import find_packages, setup

VERSION = "0.0.1"

setup(
    name="jac-mini",
    version=VERSION,
    packages=find_packages(include=["jac_mini", "jac_mini.*"]),
    install_requires=[
        "jaclang~=0.7.17",
        "fastapi~=0.111.0",
        "pydantic~=2.8.2",
        "python-dotenv~=1.0.1",
        "uvicorn~=0.30.1",
        "orjson~=3.10.6",
        "python-multipart~=0.0.9",
        "asyncer~=0.0.8",
        "fakeredis~=2.24.1",
    ],
    package_data={},
    entry_points={
        "jac": [
            "jac = jac_mini.plugin.jaseci:JacPlugin",
            "serve = jac_mini.plugin.cli:JacCmd",
        ],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jac-mini",
)
