from setuptools import setup, find_packages
from os.path import join


# def get_ver():
#    with open(join("./jaseci_ai_kit", "VERSION")) as version_file:
#        return version_file.read().strip()


setup(
    name="jaseci-vision",
    version=get_ver(),
    packages=find_packages(include=["vision", "vision.*"]),
    install_requires=[
        "jaseci",
    ],
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
