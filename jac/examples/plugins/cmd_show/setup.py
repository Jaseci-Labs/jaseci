"""Jaclang setup file."""

from setuptools import find_packages, setup  # type: ignore


VERSION = "0.0.1"

setup(
    name="cmd-show",
    version=VERSION,
    packages=find_packages(include=["cmd_show", "cmd_show.*"]),
    install_requires=["pygments"],
    package_data={
        "": ["*.ini"],
    },
    entry_points={
        "jac": ["create_cmd = cmd_show.show:"],
    },
    author="Sivasuthan S",
    author_email="sivasuthan.sukumar@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaclang",
)
