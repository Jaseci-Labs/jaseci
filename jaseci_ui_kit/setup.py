from setuptools import setup, find_packages
from os.path import join


def get_ver():
    with open(join("./jaseci_ui_kit", "VERSION")) as version_file:
        return version_file.read().strip()


setup(
    name="jaseci_ui_kit",
    version=get_ver(),
    packages=find_packages(include=["jaseci_ui_kit", "jaseci_ui_kit.*"]),
    install_requires=[
        "jaseci",
    ],
    package_data={
        "": ["VERSION"],
    },
)
