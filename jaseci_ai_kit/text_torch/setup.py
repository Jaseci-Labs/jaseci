from setuptools import setup, find_packages
from os.path import join


# def get_ver():
#    with open(join("./jaseci_ai_kit", "VERSION")) as version_file:
#        return version_file.read().strip()


setup(
    name="jaseci-text-torch",
    version=get_ver(),
    packages=find_packages(include=["text-torch", "text-torch.*"]),
    install_requires=[
        "jaseci",
        "transformers[torch]",
    ],
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
