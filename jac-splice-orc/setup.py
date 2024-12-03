from setuptools import setup, find_packages

setup(
    name="jac-splice-orc",
    version="0.1.0",
    description="JAC Splice-Orchestrator: Kubernetes-based dynamic remote module management for JacLang",
    author="Jason Mars",
    author_email="jason@jaseci.org",
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
    ],
    entry_points={
        "jac": [
            "splice_orc = jac_splice_orc.plugin.splice_plugin:SpliceOrcPlugin",
        ],
    },
    python_requires=">=3.11",
)
