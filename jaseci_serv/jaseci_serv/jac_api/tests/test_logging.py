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
from jaseci.extens.svc.elastic_svc import LOG_QUEUES, format_elastic_record


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
        JsOrcSettings.ELASTIC_CONFIG["under_test"] = True
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
        JsOrcSettings.ELASTIC_CONFIG["under_test"] = False
        JsOrc.svc_reset("elastic")
        JsOrc.svc_reset("kube")
        self.logger_off()

    def test_elastic_logging_objects(self):
        """Test sentinel register and walker run is logged properly"""
        self.logger_on()
        jac_file = open(os.path.dirname(__file__) + "/general.jac").read()
        payload = {"op": "sentinel_register", "name": "general", "code": jac_file}
        self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # There should be two entries in the log queue
        log_queue = LOG_QUEUES["core"]
        self.assertEqual(log_queue.qsize(), 2)

        # Validate the first entry
        record = log_queue.get_nowait()
        elastic_record = format_elastic_record(record)

        self.assertEqual(
            set(elastic_record.keys()),
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

        # Validate the second entry
        record = log_queue.get_nowait()
        elastic_record = format_elastic_record(record)

        self.assertEqual(
            set(elastic_record.keys()),
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

        # Validate walker run
        # Walker run will have walker_name and success in the log record
        payload = {"op": "walker_run", "name": "here_fix_create"}
        self.auth_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # There should be two entries in the log queue
        log_queue = LOG_QUEUES["core"]
        self.assertEqual(log_queue.qsize(), 2)

        # Validate the first entry
        record = log_queue.get_nowait()
        elastic_record = format_elastic_record(record)

        self.assertEqual(
            set(elastic_record.keys()),
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
                    "walker_name",
                ]
            ),
        )

        # Validate the second entry
        record = log_queue.get_nowait()
        elastic_record = format_elastic_record(record)

        self.assertEqual(
            set(elastic_record.keys()),
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
                    "walker_name",
                    "success",
                ]
            ),
        )

        self.logger_off()
