import os
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

from jaseci.jsorc.jsorc import JsOrc
from kubernetes import config as kubernetes_config, client
from unittest.mock import patch, Mock
from jaseci.jsorc.jsorc_settings import JsOrcSettings


class LoggingTests(TestCaseHelper, TestCase):
    """Test logging with jac API request"""

    @patch.object(client.ApiClient, "call_api")
    @patch.object(kubernetes_config, "load_incluster_config")
    def setUp(self, mock_config, mock_call_api):
        super().setUp()
        self.client = APIClient()
        get_user_model().objects.create_user(
            "throwawayJSCITfdfdEST_test@jaseci.com", "password"
        )
        self.user = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(self.user)
        self.suser = get_user_model().objects.create_superuser(
            "JSCITfdfdEST_test2@jaseci.com", "password", name="Administrator"
        )
        self.sauth_client = APIClient()
        self.sauth_client.force_authenticate(self.suser)

        JsOrcSettings.KUBE_CONFIG["enabled"] = True
        JsOrcSettings.ELASTIC_CONFIG["enabled"] = True
        self.kube = JsOrc.svc("kube")
        with patch.object(self.kube, "read") as mock_read, patch.object(
            self.kube, "patch"
        ) as mock_patch, patch.object(self.kube, "create") as mock_create, patch(
            "jaseci.extens.svc.elastic_svc.Elastic._get"
        ) as mocked_get:
            mocked_get.return_value = {"timed_out": False}
            mock_read.return_value = Mock()
            mock_patch.return_value = Mock()
            mock_create.return_value = Mock()
            JsOrc.svc_reset("elastic")

    def tearDown(self):
        super().tearDown()
        JsOrcSettings.KUBE_CONFIG["enabled"] = False
        JsOrcSettings.ELASTIC_CONFIG["enabled"] = False
        JsOrc.svc_reset("elastic")
        JsOrc.svc_reset("kube")
        self.logger_off()

    def test_elastic_logging_objects(self):
        """Test sentinel register and walker run is logged properly"""
        with patch("jaseci.extens.svc.elastic_svc.Elastic._post") as mocked_es_post:
            self.logger_on()
            zsb_file = open(os.path.dirname(__file__) + "/general.jac").read()
            payload = {"op": "sentinel_register", "name": "general", "code": zsb_file}
            self.auth_client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
            self.assertEqual(mocked_es_post.call_count, 2)
            pre_request_args, _ = mocked_es_post.call_args_list[0]
            self.assertEqual(pre_request_args[0], "/core/_doc?")
            self.assertEqual(
                set(pre_request_args[1].keys()),
                set(
                    [
                        "@timestamp",
                        "message",
                        "level",
                        "api_name",
                        "caller_name",
                        "caller_jid",
                        "request_user_agent",
                        "request_payload",
                    ]
                ),
            )

            post_request_args, _ = mocked_es_post.call_args_list[1]
            self.assertEqual(post_request_args[0], "/core/_doc?")
            self.assertEqual(
                set(post_request_args[1].keys()),
                set(
                    [
                        "@timestamp",
                        "message",
                        "level",
                        "api_name",
                        "request_latency",
                        "objects_touched",
                        "redis_touches",
                        "db_touches",
                        "objects_touched_size",
                        "objects_saved",
                        "caller_name",
                        "caller_jid",
                        "api_response",
                    ]
                ),
            )
            self.logger_off()
