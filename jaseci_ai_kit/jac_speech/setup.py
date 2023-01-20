from setuptools import setup, find_packages
from os.path import join

MODULES = ["stt", "tts", "vc_tts"]


def get_ver():
    with open(join("./jac_speech", "VERSION")) as version_file:
        return version_file.read().strip()


def get_extras_requires():
    extras_requires = {"all": []}
    for module in MODULES:
        with open(join("./jac_speech", module, "requirements.txt")) as req_file:
            extras_requires[module] = req_file.read().splitlines()
            extras_requires["all"].extend(extras_requires[module])
    return extras_requires


setup(
    name="jac_speech",
    version=get_ver(),
    packages=find_packages(include=["jac_speech", "jac_speech.*"]),
    install_requires=["jaseci", "pytest>=7.0.1,<7.1", "pytest-order>=1.0.1,<1.1"],
    extras_require=get_extras_requires(),
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml", "requirements.txt"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
