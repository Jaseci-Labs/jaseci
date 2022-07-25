from setuptools import setup, find_packages

setup(
    name="jaseci_kit",
    version="1.3.3.22",
    packages=find_packages(include=["jaseci_kit", "jaseci_kit.*"]),
    install_requires=[
        "jaseci",
        "tensorflow >= 2.8.0, < 3.0.0",
        "tensorflow-hub >= 0.12.0, < 1.0.0",
        "tensorflow-text >= 2.7.3, < 3.0.0",
        "transformers == 4.16.2",
        "torch >= 1.10.2, < 2.0.0",
        "pandas>=1.4.1,<2.0.0",
        "flair == 0.10",
        "numpy >= 1.22.1, < 2.0.0",
        "fasttext >=0.9.2, < 0.10.0",
        "spacy == 3.3.0",
        "sumy >= 0.9.0, < 0.10.0",
        "PyPDF2 >= 1.27.12, < 1.28",
    ],
    package_data={
        "": ["*.json", "*.cfg"],
    },
)
