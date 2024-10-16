import pytest
from fastapi.testclient import TestClient
from unittest import mock

# Mock gRPC imports to avoid ImportError in test environment
with mock.patch.dict(
    "sys.modules",
    {
        "grpc_local": mock.MagicMock(),
        "grpc_local.module_service_pb2": mock.MagicMock(),
        "grpc_local.module_service_pb2_grpc": mock.MagicMock(),
    },
):
    from managers.pod_manager import app, PodManager  # Import your FastAPI app

client = TestClient(app)


@pytest.fixture
def mock_kubernetes_and_grpc():
    with mock.patch(
        "kubernetes.config.load_incluster_config"
    ) as mock_load_incluster_config, mock.patch(
        "kubernetes.client.CoreV1Api"
    ) as mock_v1_api, mock.patch.object(
        PodManager, "create_pod"
    ) as mock_create_pod, mock.patch.object(
        PodManager, "delete_pod"
    ) as mock_delete_pod, mock.patch.object(
        PodManager, "forward_to_pod"
    ) as mock_forward_to_pod:

        # Mock load_incluster_config to avoid loading in-cluster config during tests
        mock_load_incluster_config.return_value = None

        # Mock Kubernetes CoreV1Api methods
        mock_v1_api.return_value = mock.Mock()

        # Mock responses for Kubernetes actions
        mock_create_pod.return_value = {
            "message": "Pod numpy-pod and service numpy-service created."
        }
        mock_delete_pod.return_value = {
            "message": "Pod numpy-pod and service numpy-service deleted."
        }

        # Mock gRPC method call to return expected value
        mock_forward_to_pod.return_value = "[1, 2, 3, 4]"

        yield


def test_create_pod(mock_kubernetes_and_grpc):
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


def test_run_module(mock_kubernetes_and_grpc):
    response = client.post(
        "/run_module?module_name=numpy&method_name=array", json={"args": [1, 2, 3, 4]}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "[1, 2, 3, 4]"  # Expected output from gRPC mock


def test_delete_pod(mock_kubernetes_and_grpc):
    response = client.delete("/delete_pod/numpy")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Pod numpy-pod and service numpy-service deleted."
    }
