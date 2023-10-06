from setuptools import setup, find_packages
from os.path import join


def get_ver():
    with open(join("./jaseci", "VERSION")) as version_file:
        return version_file.read().strip()


setup(
    name="jaseci",
    version=get_ver(),
    packages=find_packages(include=["jaseci", "jaseci.*"]),
    install_requires=[
        "click>=8.1.0,<8.2.0",
        "click-shell>=2.1,<2.2",
        "numpy>=1.23.0,<1.24.0",
        "antlr4-python3-runtime>=4.9.3,<4.10.0",
        "fastapi[all]>=0.75.0,<1.0.0",
        "requests",
        "redis",
        "celery>=5,<6",
        "flake8",
        "pep8-naming",
        "stripe",
        "pydantic<2.0.0",
        "docstring-parser",
        "prometheus_api_client==0.5.1",
        "prometheus-client==0.14.1",
        "kubernetes==23.6.0",
        "pytest",
        "pytest-xdist",
        "pytest-cov",
        "validators==0.21.2",
        "psycopg2-binary==2.9.5",
        "pygls==1.0.2",
        "mock",
        "beautifulsoup4>=4.12.2, <4.13.0",
        "lxml>=4.9.2, <4.10.0",
        "html5lib>=1.1, <1.2",
        "prettytable>=3.7.0, <3.8.0",
        "apache-libcloud==3.7.0",
    ],
    package_data={
        "": ["*.ini", "*.yaml", "jac.g4", "VERSION"],
    },
    entry_points={
        "console_scripts": [
            "jsctl = jaseci.cli_tools.jsctl:jsctl",
            "jac = jaseci.cli_tools.jsctl:jac",
        ]
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
