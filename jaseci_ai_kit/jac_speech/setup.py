from setuptools import setup, find_packages
from setuptools.command.install import install
from os.path import join
from sys import executable as PYTHON_PATH
import subprocess

MODULES = ["stt", "vc_tts"]
ORDEREDREQS = ["TTS==0.12.0"]


class InstallTTS(install):
    def run(self):
        subprocess.run(
            [
                PYTHON_PATH,
                "-m",
                "pip",
                "install",
                "TTS @ git+https://github.com/coqui-ai/TTS.git@090cadf270711a61e3396f2f31eaaad54e32b5c1",
            ]
        )
        super().run()


def get_extras_requires():
    extras_requires = {"all": []}
    for module in MODULES:
        with open(join("./jac_speech", module, "requirements.txt")) as req_file:
            extras_requires[module] = req_file.read().splitlines()
            extras_requires["all"].extend(extras_requires[module])
    return extras_requires


def get_ver():
    with open(join("./jac_speech", "VERSION")) as version_file:
        return version_file.read().strip()


setup(
    name="jac_speech",
    version=get_ver(),
    packages=find_packages(include=["jac_speech", "jac_speech.*"]),
    install_requires=["jaseci", "pytest>=7.0.1,<7.1", "pytest-order>=1.0.1,<1.1"],
    cmdclass={"install": OrderedInstall},
    extras_require=get_extras_requires(),
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml", "requirements.txt", "*.jac"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
