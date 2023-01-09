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
        "tensorflow>=2.8.0,<3.0.0",
        "tensorflow-hub>=0.12.0,<1.0.0",
        "tensorflow-text>=2.7.3,<3.0.0",
        "transformers==4.25.1",
        "torch>=1.10.2,<2.0.0",
        "pandas>=1.4.1,<2.0.0",
        "flair==0.11.3",
        "numpy>=1.23.0,<1.24.0",
        "fasttext>=0.9.2,<0.10.0",
        "spacy==3.3.0",
        "sumy==0.11.0",
        "PyPDF2>=1.27.12,<1.28",
        "evaluate>=0.2.2,<0.3",
        "seqeval>=1.2.2,<1.3",
        "pytest>=7.0.1,<7.1",
        "pytest-order>=1.0.1,<1.1",
        "sentence-transformers>=2.2.0,<2.3",
        "beautifulsoup4 >= 4.10.0, < 4.11.0",
        "umap-learn==0.5.3",
        "hdbscan==0.8.29",
        "librosa==0.9.2",
        "protobuf>=3.20.1,<3.21",
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
