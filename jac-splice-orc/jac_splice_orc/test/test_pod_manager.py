import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from kubernetes.client import (
    V1Pod,
    V1Condition,
    V1Service,
    V1PodStatus,
    V1ObjectMeta,
    V1PodSpec,
    V1Status,
)
from kubernetes.client.rest import ApiException
from datetime import datetime, timezone
import os

# Mock gRPC imports
with patch.dict(
    "sys.modules",
    {
        "grpc_local": MagicMock(),
        "grpc_local.module_service_pb2": MagicMock(),
        "grpc_local.module_service_pb2_grpc": MagicMock(),
    },
):
    from ..managers.pod_manager import app, PodManager

client = TestClient(app)


def create_v1_condition(type, status):
    return V1Condition(
        type=type,
        status=status,
        last_transition_time=datetime.now(timezone.utc),
        message="Condition stable",
        reason="TestingCondition",
        observed_generation=1,
    )


def mock_create_requirements_file(pod_manager, module_name, module_config):
    req_path = "/tmp/requirements.txt"
    deps = module_config.get("dependency", [])
    with open(req_path, "w") as f:
        for dep in deps:
            f.write(dep + "\n")
    return req_path


@pytest.fixture
def mock_kubernetes():
    with patch(
        "kubernetes.config.load_incluster_config"
    ) as mock_load_incluster_config, patch(
        "kubernetes.client.CoreV1Api"
    ) as mock_core_v1_api:
        mock_load_incluster_config.return_value = None
        mock_v1_api_instance = mock_core_v1_api.return_value

        def pod_read_side_effect(name, namespace, *args, **kwargs):
            if name == "numpy-pod":
                if not hasattr(pod_read_side_effect, "called"):
                    pod_read_side_effect.called = True
                    raise ApiException(status=404, reason="Not Found")
                else:
                    return V1Pod(
                        metadata=V1ObjectMeta(name="numpy-pod"),
                        spec=V1PodSpec(containers=[]),
                        status=V1PodStatus(
                            phase="Running",
                            conditions=[
                                create_v1_condition(type="Ready", status="True")
                            ],
                        ),
                    )
            raise ApiException(status=404, reason="Not Found")

        pod_read_side_effect.calls = 0
        mock_v1_api_instance.read_namespaced_pod.side_effect = pod_read_side_effect

        # ConfigMap read -> always 404 to force creation
        mock_v1_api_instance.read_namespaced_config_map.side_effect = ApiException(
            status=404, reason="Not Found"
        )

        # Creating configmap returns a mock success
        mock_v1_api_instance.create_namespaced_config_map.return_value = MagicMock()

        # Creating pod returns a Running pod
        mock_v1_api_instance.create_namespaced_pod.return_value = V1Pod(
            metadata=V1ObjectMeta(name="numpy-pod"),
            spec=V1PodSpec(containers=[]),
            status=V1PodStatus(
                phase="Running",
                conditions=[create_v1_condition(type="Ready", status="True")],
            ),
        )

        # Creating service returns a mock service
        mock_v1_api_instance.create_namespaced_service.return_value = V1Service(
            metadata=V1ObjectMeta(name="numpy-service"), spec=MagicMock()
        )

        # Deletion returns success statuses
        mock_v1_api_instance.delete_namespaced_pod.return_value = V1Status(
            message="Pod numpy-pod deleted successfully."
        )
        mock_v1_api_instance.delete_namespaced_service.return_value = V1Status(
            message="Service numpy-service deleted successfully."
        )

        yield mock_v1_api_instance


@patch.object(
    PodManager,
    "create_requirements_file",
    side_effect=mock_create_requirements_file,
    autospec=True,
)
@patch("os.makedirs", return_value=None)
def test_create_pod(mock_req_file, mock_makedirs, mock_kubernetes):
    module_config = {
        "lib_mem_size_req": "100Mi",
        "dependency": ["math", "mkl"],
        "lib_cpu_req": "500m",
        "load_type": "remote",
    }
    response = client.post("/create_pod/numpy", json=module_config)
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Pod numpy-pod is already running."}


@patch.object(
    PodManager,
    "create_requirements_file",
    side_effect=mock_create_requirements_file,
    autospec=True,
)
@patch("os.makedirs", return_value=None)
def test_run_module(mock_req_file, mock_makedirs, mock_kubernetes):
    module_config = {
        "lib_mem_size_req": "100Mi",
        "dependency": ["math", "mkl"],
        "lib_cpu_req": "500m",
        "load_type": "remote",
    }

    # Ensure pod created first
    resp = client.post("/create_pod/numpy", json=module_config)
    assert resp.status_code == 200

    response = client.post(
        "/run_module?module_name=numpy&method_name=array", json={"args": [1, 2, 3, 4]}
    )
    assert response.status_code == 200


@patch.object(
    PodManager,
    "create_requirements_file",
    side_effect=mock_create_requirements_file,
    autospec=True,
)
@patch("os.makedirs", return_value=None)
def test_create_pod_with_readiness(mock_req_file, mock_makedirs, mock_kubernetes):
    module_config = {
        "lib_mem_size_req": "100Mi",
        "dependency": ["math", "mkl"],
        "lib_cpu_req": "500m",
        "load_type": "remote",
    }

    response = client.post("/create_pod/numpy", json=module_config)
    assert response.status_code == 200
    assert response.json() == {"message": "Pod numpy-pod is already running."}
