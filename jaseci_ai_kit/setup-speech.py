from setuptools import setup, find_packages
from os.path import join


def get_ver():
    with open(join("./jaseci_ai_kit", "VERSION")) as version_file:
        return version_file.read().strip()


setup(
    name="jaseci_ai_kit",
    version=get_ver(),
    packages=find_packages(include=["jaseci_ai_kit", "jaseci_ai_kit.*"]),
    install_requires=[
        "jaseci",
        "transformers==4.25.1",
        "librosa==0.9.2",
        "inflect<=6.0.2",
        "unidecode==1.3.6",
        "soundfile<=0.11.0",
        "speechbrain==0.5.13",
    ],
    package_data={
        "": ["*.json", "*.cfg", "VERSION", "*.yaml"],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
