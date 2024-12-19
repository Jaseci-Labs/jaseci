import os
from setuptools import setup, find_packages

# Read the long description from README
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jac-splice-orc",
    version="0.1.2",
    description="JAC Splice-Orchestrator: Kubernetes-based dynamic remote module management for JacLang",
    author="Jason Mars",
    author_email="jason@jaseci.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "jac_splice_orc.config": ["config.json"],
    },
    install_requires=[
        "fastapi",
        "uvicorn",
        "grpcio",
        "grpcio-tools",
        "kubernetes",
        "pydantic",
        "requests",
        "python-dotenv",
        "numpy",
        "jaclang",
    ],
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
