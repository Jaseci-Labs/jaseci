from setuptools import setup, find_packages
from os.path import join


# def get_ver():
#    with open(join("./jaseci_ai_kit", "VERSION")) as version_file:
#        return version_file.read().strip()


setup(
    name="jaseci-text-tf",
    version=get_ver(),
    packages=find_packages(include=["text-tf", "test-tf.*"]),
    install_requires=[
        "jaseci",
        "tensorflow-cpu>=2.8.0,<3.0.0",
        "tensorflow-hub>=0.12.0,<1.0.0",
        "tensorflow-text>=2.7.3,<3.0.0",
        "transformers[tf-cpu]",
    ],
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
