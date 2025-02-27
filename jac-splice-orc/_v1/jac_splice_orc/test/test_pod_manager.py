"""Tests for the pod manager module."""

from datetime import datetime, timezone
from typing import Any, Generator
from unittest import mock
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from kubernetes.client import (
    V1Condition,
    V1ObjectMeta,
    V1Pod,
    V1PodSpec,
    V1PodStatus,
    V1Service,
    V1Status,
)
from kubernetes.client.rest import ApiException

import pytest

# Mock gRPC imports to avoid ImportError in test environment
with mock.patch.dict(
    "sys.modules",
    {
        "grpc_local": mock.MagicMock(),
        "grpc_local.module_service_pb2": mock.MagicMock(),
        "grpc_local.module_service_pb2_grpc": mock.MagicMock(),
    },
):
    from ..managers.pod_manager import app, PodManager

client = TestClient(app)


def create_condition_ready(status: str) -> V1Condition:
    """Create a ready condition for testing.

    Args:
        status: Status of the condition

    Returns:
        A V1Condition object
    """
    return V1Condition(
        type="Ready",
        status=status,
        last_transition_time=datetime.now(timezone.utc),
        reason="TestingCondition",
        message="Condition simulation",
    )


@pytest.fixture
def mock_kubernetes_and_grpc() -> Generator[None, None, None]:
    """Mock Kubernetes and gRPC for testing.

    Yields:
        None
    """
    with mock.patch(
        "kubernetes.config.load_incluster_config"
    ) as mock_load_incluster_config, mock.patch(
        "kubernetes.client.CoreV1Api"
    ) as mock_core_v1_api, mock.patch.object(
        PodManager, "create_pod"
    ) as mock_create_pod, mock.patch.object(
        PodManager, "delete_pod"
    ) as mock_delete_pod, mock.patch.object(
        PodManager, "forward_to_pod"
    ) as mock_forward_to_pod, mock.patch.object(
        PodManager, "get_pod_service_ip"
    ) as mock_get_pod_service_ip:

        mock_load_incluster_config.return_value = None

        mock_v1_api_instance = mock_core_v1_api.return_value

        call_count = [0]

        def read_pod_side_effect(
            name: str, namespace: str, *args: Any, **kwargs: Any  # noqa: ANN401
        ) -> V1Pod:
            """Side effect function for read_namespaced_pod.

            Args:
                name: Name of the pod
                namespace: Namespace of the pod
                *args: Additional positional arguments
                **kwargs: Additional keyword arguments

            Returns:
                A V1Pod object

            Raises:
                ApiException: If the pod is not found
            """
            if name == "numpy-pod":
                if call_count[0] == 0:
                    call_count[0] += 1
                    # First check: pod phase = Pending, not ready yet
                    return V1Pod(
                        metadata=V1ObjectMeta(name="numpy-pod"),
                        spec=V1PodSpec(containers=[]),
                        status=V1PodStatus(phase="Pending", conditions=[]),
                    )
                else:
                    # Second check: pod is now Running and Ready
                    return V1Pod(
                        metadata=V1ObjectMeta(name="numpy-pod"),
                        spec=V1PodSpec(containers=[]),
                        status=V1PodStatus(
                            phase="Running", conditions=[create_condition_ready("True")]
                        ),
                    )
            raise ApiException(status=404, reason="Not Found")

        mock_v1_api_instance.read_namespaced_pod.side_effect = read_pod_side_effect

        mock_v1_api_instance.read_namespaced_config_map.side_effect = ApiException(
            status=404, reason="Not Found"
        )

        mock_v1_api_instance.create_namespaced_config_map.return_value = MagicMock()

        mock_v1_api_instance.create_namespaced_pod.return_value = V1Pod(
            metadata=V1ObjectMeta(name="numpy-pod"),
            spec=V1PodSpec(containers=[]),
            status=V1PodStatus(phase="Pending", conditions=[]),
        )

        mock_v1_api_instance.create_namespaced_service.return_value = V1Service(
            metadata=V1ObjectMeta(name="numpy-service")
        )

        mock_v1_api_instance.delete_namespaced_pod.return_value = V1Status(
            message="Pod numpy-pod deleted successfully."
        )
        mock_v1_api_instance.delete_namespaced_service.return_value = V1Status(
            message="Service numpy-service deleted successfully."
        )

        mock_create_pod.return_value = {
            "message": "Pod numpy-pod and service numpy-service created."
        }
        mock_delete_pod.return_value = {
            "message": "Pod numpy-pod and service numpy-service deleted."
        }
        mock_get_pod_service_ip.return_value = "127.0.0.1"
        mock_forward_to_pod.return_value = "[1, 2, 3, 4]"

        yield


def test_create_pod(mock_kubernetes_and_grpc: None) -> None:
    """Test creating a pod.

    Args:
        mock_kubernetes_and_grpc: Fixture for mocking Kubernetes and gRPC
    """
    module_config = {
        "numpy": {
            "lib_mem_size_req": "100MB",
            "dependency": ["math", "mkl"],
            "lib_cpu_req": "500m",
            "load_type": "remote",
        }
    }
    response = client.post("/create_pod/numpy", json={"module_config": module_config})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Pod numpy-pod and service numpy-service created."
    }


def test_run_module(mock_kubernetes_and_grpc: None) -> None:
    """Test running a module.

    Args:
        mock_kubernetes_and_grpc: Fixture for mocking Kubernetes and gRPC
    """
    response = client.post(
        "/run_module?module_name=numpy&method_name=array", json={"args": [1, 2, 3, 4]}
    )
    assert response.status_code == 200
    assert response.json() == "[1, 2, 3, 4]"


def test_delete_pod(mock_kubernetes_and_grpc: None) -> None:
    """Test deleting a pod.

    Args:
        mock_kubernetes_and_grpc: Fixture for mocking Kubernetes and gRPC
    """
    response = client.delete("/delete_pod/numpy")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Pod numpy-pod and service numpy-service deleted."
    }
