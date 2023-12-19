from setuptools import setup, find_packages
from os.path import join


def get_ver():
    with open(join("./jaseci_socket", "VERSION")) as version_file:
        return version_file.read().strip()


setup(
    name="jaseci_socket",
    version=get_ver(),
    packages=find_packages(),
    install_requires=["websockets", "redis", "orjson", "rel", "bcrypt"],
    package_data={
        "": ["VERSION"],
    },
    scripts=["jssocket"],
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
