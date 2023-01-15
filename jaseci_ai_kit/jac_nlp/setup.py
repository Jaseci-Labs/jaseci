from setuptools import setup, find_packages
from os.path import join

MODULES = ["bart_sum", "cl_summer", "ent_ext", "fast_enc", "sbert_sim", "t5_sum"]

def get_ver():
    with open("VERSION") as version_file:
        return version_file.read().strip()


def get_extras_requires():
    extras_requires = {"all": MODULES}
    for module in MODULES:
        with open(join("jac_nlp", module, "requirements.txt")) as req_file:
            extras_requires[module] = req_file.read().splitlines()
    return extras_requires


setup(
    name="jac_nlp",
    version=get_ver(),
    packages=find_packages(include=["jac_nlp", "jac_nlp.*"]),
    install_requires=["jaseci", "pytest>=7.0.1,<7.1", "pytest-order>=1.0.1,<1.1"],
    extras_require=get_extras_requires(),
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci/jaseci_ai_kit/jac_nlp",
)
