"""Jaclang setup file."""

from setuptools import find_packages, setup

VERSION = "0.2.0"

setup(
    name="jaclang-jaseci",
    version=VERSION,
    packages=find_packages(include=["jaclang_jaseci", "jaclang_jaseci.*"]),
    install_requires=[
        "jaclang==0.7.17",
        "fastapi==0.111.0",
        "pydantic==2.8.2",
        "pymongo==4.8.0",
        "motor==3.5.0",
        "motor-types==1.0.0b4",
        "python-dotenv==1.0.1",
        "uvicorn==0.30.1",
        "pyjwt[crypto]==2.8.0",
        "passlib==1.7.4",
        "types-passlib==1.7.7.20240327",
        "email-validator==2.2.0",
        "orjson==3.10.6",
        "redis==5.0.7",
        "types-redis==4.6.0.20240425",
        "python-multipart==0.0.9",
        "httpx==0.27.0",
        "sendgrid==6.11.0",
        "fastapi-sso==0.15.0",
        "google-auth==2.32.0",
        "asyncer==0.0.8",
    ],
    package_data={},
    entry_points={
        "jac": ["jac = jaclang_jaseci.plugin.jaseci:JacPlugin"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaclang",
)
