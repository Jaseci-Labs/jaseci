from setuptools import setup, find_packages
from setuptools.command.install import install
import atexit
import sys
import platform
import os


MODULES = ["stt", "vc_tts"]
INSTALLABLE_MODULES = []


def _post_install():
    UNSUPPORTED_MODULES = [
        module for module in MODULES if module not in INSTALLABLE_MODULES
    ]
    if UNSUPPORTED_MODULES:
        print(
            "\033[93m"
            + f"{UNSUPPORTED_MODULES} modules are not supported on your system. "
            + "\033[0m"
        )


class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


def get_ver():
    with open(os.path.join("./jac_speech", "VERSION")) as version_file:
        return version_file.read().strip()


def get_os():
    if sys.platform == "darwin" and platform.machine() == "arm64":
        return ".darwin"
    return ""


def get_extras_requires():
    extras_requires = {"all": []}
    platform = get_os()
    for module in MODULES:
        if not os.path.exists(
            os.path.join("jac_speech", module, f"requirements{platform}.txt")
        ):
            continue
        with open(
            os.path.join("jac_speech", module, f"requirements{platform}.txt")
        ) as req_file:
            extras_requires[module] = req_file.read().splitlines()
            extras_requires["all"].extend(extras_requires[module])
        INSTALLABLE_MODULES.append(module)
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
    cmdclass={"install": new_install},
)
