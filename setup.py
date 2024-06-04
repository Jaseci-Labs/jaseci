"""Jaclang setup file."""

from __future__ import annotations

from jaclang.compiler import generate_static_parser

from setuptools import find_packages, setup  # type: ignore


generate_static_parser(force=True)


VERSION = "0.6.0"

setup(
    name="jaclang",
    version=VERSION,
    packages=find_packages(include=["jaclang", "jaclang.*"]),
    install_requires=[],
    package_data={
        "": ["*.ini", "*.lark"],
    },
    extras_require={
        "llms": [
            "transformers",
            "accelerator",
            "torch",
            "ollama",
            "anthropic",
            "groq",
            "openai",
            "together",
            "loguru",
        ]
    },
    entry_points={
        "console_scripts": [
            "jac = jaclang.cli.cli:start_cli",
        ],
    },
    author="Jason Mars",
    author_email="jason@jaseci.org",
    url="https://github.com/Jaseci-Labs/jaclang",
    long_description=open("README.md").read(),  # noqa
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
    description="Jaclang is a unique and powerful programming language that runs on top of Python, offering an unprecedented level of intelligence and intuitive understanding.",  # noqa
)
