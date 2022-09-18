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
        "numpy >= 1.22.3, < 1.23.0",
        "antlr4-python3-runtime>=4.9.3,<4.10.0",
        "fastapi[all]>=0.75.0,<1.0.0",
        "requests",
        "redis",
        "celery>=5,<6",
        "flake8",
        "pep8-naming",
        "stripe",
        "pydantic",
        "docstring-parser",
    ],
    package_data={
        "": ["*.ini", "jac.g4", "VERSION"],
    },
    entry_points={"console_scripts": ["jsctl = jaseci.jsctl.jsctl:main"]},
)
