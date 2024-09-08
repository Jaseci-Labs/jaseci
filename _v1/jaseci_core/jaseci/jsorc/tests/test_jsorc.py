from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.test_core import CoreTest
from unittest.mock import patch, Mock
from kubernetes import config as kubernetes_config, client
from jaseci.jsorc.jsorc_settings import JsOrcSettings
from .fixture.elastic_resources import ELASTIC_RESOURCES
from urllib3.response import HTTPResponse


def aggregate_k8s_resources(mocked):
    """Aggregate k8s resources from multiple mocked calls to kube"""
    resources = {}
    call_args_list = mocked.call_args_list
    for call_args in call_args_list:
        args, _ = call_args
        # arg1: kind, arg2: name
        kind = args[0]
        name = args[1]
        if kind not in resources:
            resources[kind] = []
        # The resource name for Namespace is different from run to run
        if kind != "Namespace":
            resources[kind].append(name)

    return resources


class MockKubeTest(CoreTest):
    """Custom test class that mock the environment to be inside a k8s cluster"""

    @patch.object(client.ApiClient, "call_api")
    @patch.object(kubernetes_config, "load_incluster_config")
    def setUp(self, mock_config, mock_call_api):
        super().setUp()
        JsOrcSettings.KUBE_CONFIG["enabled"] = True
        JsOrcSettings.KUBE_CONFIG["namespace"] = "jsorc-unit-test"
        JsOrcSettings.ELASTIC_CONFIG["enabled"] = True
        self.kube = JsOrc.svc("kube")


class JsOrcTest(MockKubeTest):
    """Unit test for JsOrc"""

    def setUp(self):
        super().setUp()

    def test_jsorc_elastic_create(self):
        self.call(
            self.smast,
            [
                "config_update",
                {"name": "ELASTIC_CONFIG", "field_key": "enabled", "field_value": True},
            ],
        )
        with patch.object(self.kube, "read") as mock_read, patch.object(
            self.kube, "patch"
        ) as mock_patch, patch.object(self.kube, "create") as mock_create:
            # resource do not exist
            mocked_response = HTTPResponse(status=404)
            mock_read.return_value = mocked_response
            mock_patch.return_value = Mock()
            mock_create.return_value = Mock()

            JsOrc.svc_reset("elastic")

            # Mocking elastic health check to show its up and running
            with patch("jaseci.extens.svc.elastic_svc.Elastic._get") as mocked_get:
                mocked_get.return_value = {"timed_out": False}
                JsOrc.regenerate()

            read_resources = aggregate_k8s_resources(mock_read)
            assert read_resources == ELASTIC_RESOURCES

            create_resources = aggregate_k8s_resources(mock_create)
            assert create_resources == ELASTIC_RESOURCES

            # No resources should be patched
            assert not mock_patch.called

    def test_jsorc_elastic_patch(self):
        self.call(
            self.smast,
            [
                "config_update",
                {"name": "ELASTIC_CONFIG", "field_key": "enabled", "field_value": True},
            ],
        )
        with patch.object(self.kube, "read") as mock_read, patch.object(
            self.kube, "patch"
        ) as mock_patch, patch.object(self.kube, "create") as mock_create:
            mock_read.return_value = Mock()
            mock_patch.return_value = Mock()
            mock_create.return_value = Mock()

            JsOrc.svc_reset("elastic")

            # Mocking elastic health check to show its up and running
            with patch("jaseci.extens.svc.elastic_svc.Elastic._get") as mocked_get:
                mocked_get.return_value = {"timed_out": False}
                JsOrc.regenerate()

            read_resources = aggregate_k8s_resources(mock_read)
            assert read_resources == ELASTIC_RESOURCES

            patch_resources = aggregate_k8s_resources(mock_patch)
            # No need to patch Namespace
            del ELASTIC_RESOURCES["Namespace"]

            assert patch_resources == ELASTIC_RESOURCES

            # No resources should be created
            assert not mock_create.called
