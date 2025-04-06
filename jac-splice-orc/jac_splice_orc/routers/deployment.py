"""This module provides a FastAPI-based API for managing Kubernetes pods."""

from os import getenv
from re import compile
from typing import Any

from fastapi import APIRouter

from ..dtos.deployment import (
    Deployment,
    DeploymentResponse,
    DryRunResponse,
    Placeholder,
)
from ..services.kubernetes import KubernetesService

PLACEHOLDER = compile(r"\$g{([^\^:}]+)(?:\:([^\}]+))?}")
CLUSTER_WIDE = getenv("CLUSTER_WIDE") == "true"

router = APIRouter(prefix="/deployment")


@router.get("")
def get_deployments() -> dict:
    """Get all deployments."""
    return KubernetesService.get_modules()


@router.post("")
def deployment(deployment: Deployment) -> DeploymentResponse:
    """Deploy module with configs."""
    module_path, dependencies_path = KubernetesService.get_module_paths(deployment)

    config1: dict[str, Any] = {}
    response = DeploymentResponse(deployment=deployment)
    if dependencies_path.is_dir():
        output, config1 = KubernetesService.apply_manifests(
            dependencies_path, deployment.config
        )
        response.dependencies.push(output)

    output, config2 = KubernetesService.apply_manifests(module_path, deployment.config)
    response.modules.push(output)

    deployment.config = {**config1, **config2}

    KubernetesService.update_modules(deployment)

    return response


@router.post("/dry_run")
def dry_run(deployment: Deployment) -> DryRunResponse:
    """Delete the pod and service for the given module and return the result."""
    module_path, dependencies_path = KubernetesService.get_module_paths(deployment)

    response = DryRunResponse()
    if dependencies_path.is_dir():
        raw_manifests, placeholders = KubernetesService.view_manifests(
            dependencies_path, deployment.config
        )
        response.dependencies = raw_manifests
        response.placeholders.update(
            {key: Placeholder(**value) for key, value in placeholders.items()}
        )

    raw_manifests, placeholders = KubernetesService.view_manifests(
        module_path, deployment.config
    )
    response.modules = raw_manifests
    response.placeholders.update(
        {key: Placeholder(**value) for key, value in placeholders.items()}
    )

    return response
