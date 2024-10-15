"""Jaclang setup file."""

from setuptools import find_packages, setup

VERSION = "0.1.4"

setup(
    name="jac-cloud",
    version=VERSION,
    packages=find_packages(include=["jac_cloud", "jac_cloud.*"]),
    install_requires=[
        "jaclang~=0.7.23",
        "fastapi~=0.111.0",
        "pydantic~=2.8.2",
        "pymongo~=4.8.0",
        "motor~=3.5.0",
        "motor-types~=1.0.0b4",
        "python-dotenv~=1.0.1",
        "uvicorn~=0.30.1",
        "pyjwt[crypto]~=2.8.0",
        "passlib~=1.7.4",
        "types-passlib~=1.7.7.20240327",
        "email-validator~=2.2.0",
        "orjson~=3.10.6",
        "redis~=5.0.7",
        "types-redis~=4.6.0.20240425",
        "python-multipart~=0.0.9",
        "httpx~=0.27.0",
        "sendgrid~=6.11.0",
        "fastapi-sso~=0.15.0",
        "google-auth~=2.32.0",
        "asyncer~=0.0.8",
        "fakeredis~=2.24.1",
        "ecs-logging~=2.2.0",
    ],
    package_data={},
    entry_points={
        "jac": [
            "jac = jac_cloud.plugin.jaseci:JacPlugin",
            "serve = jac_cloud.plugin.cli:JacCmd",
        ],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jac-cloud",
)
