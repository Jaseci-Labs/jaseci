from setuptools import setup, find_packages

setup(
    name="jac-splice-orc",
    version="0.1.0",
    description="JAC Splice-Orchestrator: Kubernetes-based dynamic remote module management for JacLang",
    author="Jason Mars",
    author_email="jason@jaseci.org",
    packages=find_packages(),
    install_requires=[
        "jaclang~=0.7.17",
        "fastapi",
        "uvicorn",
        "grpcio",
        "grpcio-tools",
        "kubernetes",
        "pydantic",
    ],
    entry_points={
        "jac": [
            "splice_orc = plugin.splice_plugin:SpliceOrcPlugin",
        ],
    },
    python_requires=">=3.11",
)
