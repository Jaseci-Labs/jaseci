from setuptools import setup, find_packages
from os.path import join

MODULES = [
    "pdf_ext",
    "translator",
    "cluster",
    "ph",
    "openai",
    "huggingface",
    "langchain",
    "forecast",
]


def get_ver():
    with open(join("./jac_misc", "VERSION")) as version_file:
        return version_file.read().strip()


def get_extras_requires():
    extras_requires = {"all": []}
    for module in MODULES:
        with open(join("./jac_misc", module, "requirements.txt")) as req_file:
            extras_requires[module] = req_file.read().splitlines()
            extras_requires["all"].extend(extras_requires[module])
    return extras_requires


setup(
    name="jac_misc",
    version=get_ver(),
    packages=find_packages(include=["jac_misc", "jac_misc.*"]),
    install_requires=[
        f"jaseci=={get_ver()}",
        "pytest>=7.0.1,<7.1",
        "pytest-order>=1.0.1,<1.1",
    ],
    extras_require=get_extras_requires(),
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml", "requirements.txt", "*.jac"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci/jaseci_ai_kit/jac_misc",
)
