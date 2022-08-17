from setuptools import setup, find_packages

setup(
    name="jaseci",
    version="1.3.4.4",
    packages=find_packages(include=["jaseci", "jaseci.*"]),
    install_requires=[
        "click>=8.1.0,<8.2.0",
        "click-shell>=2.1,<2.2",
        "numpy >= 1.22.3, < 1.23.0",
        "antlr4-python3-runtime>=4.9.3,<4.10.0",
        "fastapi[all]>=0.75.0,<1.0.0",
        "requests",
        "redis",
        "flake8",
        "stripe",
        "pydantic",
        "prometheus-api-client==0.5.1", 
        "prometheus-client==0.14.1",
        "kubernetes==23.6.0"
        "docstring-parser",
    ],
    package_data={
        "": ["*.ini"],
    },
    entry_points={"console_scripts": ["jsctl = jaseci.jsctl.jsctl:main"]},
)
