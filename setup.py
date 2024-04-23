"""Jaclang setup file."""

from __future__ import annotations

from setuptools import find_packages, setup


VERSION = "0.0.1"

setup(
    name="jaclang-jaseci",
    version=VERSION,
    packages=find_packages(include=["jaclang_jaseci", "jaclang_jaseci.*"]),
    install_requires=[
        "jaclang",
        "fastapi==0.109.0",
        "pydantic==2.6.0",
        "pymongo==4.6.1",
        "motor==3.3.2",
        "motor-types==1.0.0b4",
        "python-dotenv==1.0.1",
        "uvicorn==0.27.0.post1",
        "pyjwt[crypto]==2.8.0",
        "passlib[bcrypt]==1.7.4",
        "email-validator==2.1.0.post1",
        "orjson==3.9.13",
        "redis==5.0.1",
        "types-redis==4.6.0.20240218",
        "python-multipart==0.0.9",
        "httpx==0.27.0",
    ],
    package_data={},
    entry_points={
        "jac": [],
    },
    author="Jason Mars, Yiping Kang, Alexie Madolid",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaclang-jaseci",
)
