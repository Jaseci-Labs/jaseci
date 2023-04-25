from setuptools import setup, find_packages
from os.path import join
import subprocess
import sys

try:
    import pybind11
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pybind11"])
    import pybind11


MODULES = [
    "bart_sum",
    "cl_summer",
    "ent_ext",
    "fast_enc",
    "sbert_sim",
    "t5_sum",
    "text_seg",
    "tfm_ner",
    "use_enc",
    "use_qa",
    "zs_classifier",
    "bi_enc",
    "topic_ext",
    "gpt2",
    "bi_ner",
    "gpt3",
    "sentiment",
    "paraphraser",
]


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked."""

    def __init__(self, user=False):
        try:
            import pybind11
        except ImportError:
            if subprocess.call([sys.executable, "-m", "pip", "install", "pybind11"]):
                raise RuntimeError("pybind11 install failed.")

        self.user = user

    def __str__(self):
        import pybind11

        return pybind11.get_include(self.user)


def get_ver():
    with open(join("./jac_nlp", "VERSION")) as version_file:
        return version_file.read().strip()


def get_extras_requires():
    extras_requires = {"all": []}
    for module in MODULES:
        with open(join("./jac_nlp", module, "requirements.txt")) as req_file:
            extras_requires[module] = req_file.read().splitlines()
            extras_requires["all"].extend(extras_requires[module])
    return extras_requires


setup(
    name="jac_nlp",
    version=get_ver(),
    packages=find_packages(include=["jac_nlp", "jac_nlp.*"]),
    install_requires=[
        "jaseci",
        "pytest>=7.0.1,<7.1",
        "pytest-order>=1.0.1,<1.1",
    ],
    extras_require=get_extras_requires(),
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml", "requirements.txt", "*.jac"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
