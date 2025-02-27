"""This module provides a FastAPI-based API for managing Kubernetes pods."""

from os import getenv
from os.path import dirname, isdir
from pathlib import Path
from re import compile
from typing import Any

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from jac_splice_orc import manifests

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
    if CLUSTER_WIDE:
        deployment.config["namespace"] = KubernetesService.namespace

    manifest_path = dirname(manifests.__file__)
    module_path = Path(f"{manifest_path}/{deployment.module}")
    if not isdir(module_path):
        raise HTTPException(
            400, f"Deployment for {deployment.module} is not yet support!"
        )

    dependencies_path = Path(f"{module_path}/dependencies")

    config1: dict[str, Any] = {}
    response = DeploymentResponse(deployment=deployment)
    if isdir(dependencies_path):
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
    if CLUSTER_WIDE:
        deployment.config["namespace"] = KubernetesService.namespace

    manifest_path = dirname(manifests.__file__)
    module_path = Path(f"{manifest_path}/{deployment.module}")
    if not isdir(module_path):
        raise HTTPException(
            400, f"Deployment for {deployment.module} is not yet support!"
        )

    dependencies_path = Path(f"{module_path}/dependencies")

    response = DryRunResponse()
    if isdir(dependencies_path):
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
