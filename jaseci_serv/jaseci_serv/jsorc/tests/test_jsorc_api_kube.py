from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from jaseci.utils.utils import TestCaseHelper
from jaseci_serv.utils.test_utils import skip_without_kube
from django.test import TestCase
from jaseci_serv.svc import MetaService

import os
import json
import time


class JsorcAPIKubeTests(TestCaseHelper, TestCase):
    """
    Test the JSORC APIs, that require kubernetes
    """

    def setUp(self):
        super().setUp()
        self.meta = MetaService()
        # Need to reset the MetaService to load in MetaConfig
        # because DB is reset between test
        self.meta.reset()

        self.user = get_user_model().objects.create_user(
            "throwawayJSCITfdfdEST_test@jaseci.com", "password"
        )
        self.master = self.user.get_master()

        self.nonadmin = get_user_model().objects.create_user(
            "JSCITfdfdEST_test@jaseci.com", "password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.notadminc = APIClient()
        self.notadminc.force_authenticate(self.nonadmin)

        # Enable JSORC
        self.enable_jsorc()

    def enable_jsorc(self):
        payload = {"op": "config_get", "name": "META_CONFIG", "do_check": False}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        meta_config = json.loads(res.data)
        meta_config["automation"] = True
        meta_config["keep_alive"] = ["promon"]

        # Set automation to be true
        payload = {
            "op": "config_set",
            "name": "META_CONFIG",
            "value": meta_config,
            "do_check": False,
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {"op": "service_refresh", "name": "meta"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

    def tearDown(self):
        super().tearDown()

    @skip_without_kube
    def test_actions_tracking(self):
        """
        Test actions tracking API of JSORC
        """
        # Start tracking actions
        payload = {"op": "jsorc_trackact_start"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # load action
        payload = {
            "op": "jsorc_actions_config",
            "name": "test_module",
            "config": "jaseci_ai_kit.config",
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "jsorc_actions_load", "name": "test_module", "mode": "module"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # register jac file
        zsb_file = open(os.path.dirname(__file__) + "/test_jsorc.jac").read()
        payload = {"op": "sentinel_register", "name": "test_snt", "code": zsb_file}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # call the walker
        payload = {"op": "walker_run", "name": "test_actions_tracking"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # stop action tracking and assert on the result
        payload = {"op": "jsorc_trackact_stop"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue("actions_calls" in res.data[0])
        self.assertTrue("test_module.call" in res.data[0]["actions_calls"])

    @skip_without_kube
    def test_benchmark(self):
        """
        Test performance benchmark API of JSORC
        """
        # Start benchmark mode
        payload = {"op": "jsorc_benchmark_start"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # register jac file
        zsb_file = open(os.path.dirname(__file__) + "/test_jsorc.jac").read()
        payload = {"op": "sentinel_register", "name": "test_snt", "code": zsb_file}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # call the walker
        payload = {"op": "walker_run", "name": "test_benchmark"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # stop action tracking and assert on the result
        payload = {"op": "jsorc_benchmark_stop", "report": True}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue("sentinel_register" in res.data)
        self.assertTrue("walker_run" in res.data)
        self.assertTrue("test_benchmark" in res.data["walker_run"])

    @skip_without_kube
    def test_system_tracking(self):
        """
        Test system state tracking of JSORC
        """
        # Start tracking
        payload = {"op": "jsorc_tracksys_start"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        time.sleep(20)
        # stop action tracking and assert on the result
        payload = {"op": "jsorc_tracksys_stop"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue(all("prometheus" in state for state in res.data["states"]))
        self.assertTrue(all("actions" in state for state in res.data["states"]))

    @skip_without_kube
    def test_set_action_policy(self):
        """
        Test setting custom action policy in JSORC
        """
        payload = {"op": "jsorc_actionpolicy_set", "policy_name": "Evaluation"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # stop action tracking and assert on the result
        payload = {"op": "jsorc_actionpolicy_get"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.data["policy"], "Evaluation")

    @skip_without_kube
    def test_jsorc_actions_load_module(self):
        """
        Loading an action as module via jsorc
        """
        payload = {
            "op": "jsorc_actions_config",
            "name": "test_module",
            "config": "jaseci_ai_kit.config",
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "jsorc_actions_load", "name": "test_module", "mode": "module"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["action_status"]["mode"], "module")
        self.assertEqual(
            res.data["action_status"]["module"]["name"], "jaseci_ai_kit.test_module"
        )
        self.assertTrue(
            "jaseci_ai_kit.modules.test_module.test_module"
            in self.master.actions_module_list()
        )
        self.assertTrue("test_module.call" in self.master.actions_list())

    @skip_without_kube
    def test_jsorc_actions_unload_auto(self):
        """
        Unloading auto unload an action
        """
        payload = {
            "op": "jsorc_actions_config",
            "name": "test_module",
            "config": "jaseci_ai_kit.config",
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "jsorc_actions_load", "name": "test_module", "mode": "module"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertTrue("test_module.call" in self.master.actions_list())

        payload = {"op": "jsorc_actions_unload", "name": "test_module", "mode": "auto"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertFalse("test_module.call" in self.master.actions_list())
        self.assertFalse(
            "jaseci_ai_kit.modules.test_module.test_module"
            in self.master.actions_module_list()
        )

    @skip_without_kube
    def test_jsorc_actions_load_remote(self):
        """
        Loading a remote action via JSORC, jsorc will spawn a remote pod
        """
        payload = {
            "op": "jsorc_actions_config",
            "name": "test_module",
            "config": "jaseci_ai_kit.config",
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        payload = {"op": "jsorc_actions_load", "name": "test_module", "mode": "remote"}
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        while True:
            payload = {
                "op": "jsorc_actions_load",
                "name": "test_module",
                "mode": "remote",
            }
            res = self.client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
            if res.data["action_status"]["remote"]["status"] == "READY":
                break
        self.assertEqual(res.data["action_status"]["mode"], "remote")
        self.assertTrue("test_module.call" in self.master.actions_list())

    @skip_without_kube
    def test_jsorc_actions_unload_remote_and_retire_pod(self):
        """
        Test JSORC unload a remote action and retire the corresponding microservices
        """
        payload = {
            "op": "jsorc_actions_config",
            "name": "test_module",
            "config": "jaseci_ai_kit.config",
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # Load the remote action first
        while True:
            payload = {
                "op": "jsorc_actions_load",
                "name": "test_module",
                "mode": "remote",
            }
            res = self.client.post(
                reverse(f'jac_api:{payload["op"]}'), payload, format="json"
            )
            if res.data["action_status"]["remote"]["status"] == "READY":
                break
        # confirm pod is running
        self.assertTrue(
            self.meta.app.kubernetes.is_running("test-module", self.meta.app.namespace)
        )
        # actions unload will reture microservice pod by default
        payload = {
            "op": "jsorc_actions_unload",
            "name": "test_module",
            "mode": "remote",
        }
        res = self.client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )
        # check that the action is unloaded
        self.assertFalse("test_module.call" in self.master.actions_list())
        # Wait for the pod to be terminated
        # NOTE: Have to wait here because kubernetes has a 30s grace period for deleting pod
        time.sleep(35)
        # check the pod is no longer alive
        self.assertFalse(
            self.meta.app.kubernetes.is_running("test-module", self.meta.app.namespace)
        )
