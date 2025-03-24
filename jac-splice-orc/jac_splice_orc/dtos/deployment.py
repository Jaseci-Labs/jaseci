"""Jac Orc DTOs."""

from subprocess import CompletedProcess
from typing import Any

from pydantic import BaseModel, Field

ModulesType = dict[
    str,  # Namespace
    dict[
        str,  # Module
        dict[str, dict[str, Any]],  # Service / Python Library - Deployment Config
    ],
]


class Deployment(BaseModel):
    """Deployment DTO."""

    module: str
    version: str = "latest"
    config: dict[str, Any] = Field(default_factory=dict)


class DeploymentResults(BaseModel):
    """DeploymentResults DTO."""

    results: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

    def push(self, output: CompletedProcess[str]) -> None:
        """Push results and errors."""
        if results := output.stdout.strip():
            self.results += results.split("\n")

        if errors := output.stderr.strip():
            self.errors.append(errors)


class DeploymentResponse(BaseModel):
    """DeploymentResponse DTO."""

    deployment: Deployment
    dependencies: DeploymentResults = Field(default_factory=DeploymentResults)
    modules: DeploymentResults = Field(default_factory=DeploymentResults)


class Placeholder(BaseModel):
    """Placeholder DTO."""

    default: Any
    current: Any


class DryRunResponse(BaseModel):
    """DeploymentResponse DTO."""

    placeholders: dict[str, Placeholder] = Field(default_factory=dict)
    dependencies: dict[str, str] = Field(default=None)
    modules: dict[str, str] = Field(default=None)
