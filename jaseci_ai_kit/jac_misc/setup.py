from setuptools import setup, find_packages
from os.path import join

MODULES = ["pdf_ext", "translator"]


def get_ver():
    with open("VERSION") as version_file:
        return version_file.read().strip()


def get_extras_requires():
    extras_requires = {}
    for module in MODULES:
        with open(join("jac_misc", module, "requirements.txt")) as req_file:
            extras_requires[module] = req_file.read().splitlines()
    return extras_requires


setup(
    name="jac_misc",
    version=get_ver(),
    packages=find_packages(include=["jac_misc", "jac_misc.*"]),
    install_requires=["jaseci"],
    extras_require=get_extras_requires(),
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
