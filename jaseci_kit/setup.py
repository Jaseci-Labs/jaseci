from setuptools import setup, find_packages

setup(
    name="jaseci_kit",
    version="1.3.3.18",
    packages=find_packages(include=["jaseci_kit", "jaseci_kit.*"]),
    install_requires=[
        "jaseci",
        "tensorflow >= 2.8.0, < 3.0.0",
        "tensorflow-hub >= 0.12.0, < 1.0.0",
        "tensorflow-text >= 2.7.3, < 3.0.0",
        "transformers == 4.16.2",
        "torch >= 1.10.2, < 2.0.0",
        "pandas>=1.4.1,<2.0.0",
        "flair",
    ],
    package_data={
        "": ["*.json", "*.cfg"],
    },
)
