import os
from setuptools import setup, find_packages

# Read the long description from README
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jac-splice-orc",
    version="0.1.8",
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
        "fastapi~=0.111.0",
        "uvicorn~=0.30.1",
        "grpcio~=1.68.1",
        "grpcio-tools~=1.67.1",
        "kubernetes~=31.0.0",
        "pydantic~=2.8.2",
        "requests~=2.32.3",
        "python-dotenv~=1.0.1",
        "numpy~=2.0.1",
        "jaclang",
    ],
    entry_points={
        "jac": [
            "splice_orc = jac_splice_orc.plugin.splice_plugin:SpliceOrcPlugin",
        ],
    },
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
