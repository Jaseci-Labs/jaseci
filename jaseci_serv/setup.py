from setuptools import setup, find_packages
from os.path import join


def get_ver():
    with open(join("./jaseci_serv", "VERSION")) as version_file:
        return version_file.read().strip()


setup(
    name="jaseci_serv",
    version=get_ver(),
    packages=find_packages(include=["jaseci_serv", "jaseci_serv.*"]),
    install_requires=[
        "jaseci",
        "Django>=3.2.12,<3.3.0",
        "djangorestframework>=3.13.1,<3.14.0",
        "django-rest-knox>=4.2.0,<4.3.0",
        "django-rest-passwordreset>=1.2.1,<1.3.0",
        "drf-yasg>=1.20.0,<1.21.0",
        "markdown>=3.3.6,<3.4.0",
        "psycopg2-binary>=2,<3",
        "sphinx>=2.4.3,<2.5.0",
        "django-cors-headers",
        "tblib",
        "django-celery-results>=2.3,<2.4",
        "django-celery-beat>=2.2",
    ],
    package_data={
        "": ["*.jac", "VERSION"],
    },
    entry_points={"console_scripts": ["jsserv = jaseci_serv.manage:main"]},
)
