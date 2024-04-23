from setuptools import setup, find_packages
from os.path import join


def get_ver():
    with open(join("./jaseci_socket", "VERSION")) as version_file:
        return version_file.read().strip()


setup(
    name="jaseci_socket",
    version=get_ver(),
    packages=find_packages(),
    install_requires=[
        "redis==5.0.3",
        "orjson==3.9.10",
        "rel==0.4.9.1",
        "websockets==12.0",
        "bcrypt==4.1.2",
    ],
    package_data={
        "": ["VERSION"],
    },
    scripts=["jssocket"],
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaseci",
)
