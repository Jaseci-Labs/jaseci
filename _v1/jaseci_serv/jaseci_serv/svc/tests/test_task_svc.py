import os
from json import loads
from re import sub

from jaseci.utils.utils import TestCaseHelper
from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.test_core import skip_without_redis

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from jaseci_serv.base.models import JaseciObject


class TaskServiceTest(TestCaseHelper, TestCase):
    def assert_obj(self, val=None):
        # check on db if committed
        self.assertEqual(
            val,
            loads(JaseciObject.objects.get(jid=self.node_a).jsci_obj)["context"]["val"],
        )

    def setUp(self):
        super().setUp()
        # First user is always super,
        self.admin = get_user_model().objects.create_superuser(
            "admin@jaseci.com", "password"
        )
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(self.admin)
        self.admin_master = self.admin.get_master()

        self.user = get_user_model().objects.create_user("user@jaseci.com", "password")
        self.user_client = APIClient()
        self.user_client.force_authenticate(self.user)
        self.user_master = self.user.get_master()

        zsb_file = open(os.path.dirname(__file__) + "/testing.jac").read()
        payload = {"op": "sentinel_register", "name": "public", "code": zsb_file}
        self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {"op": "walker_run", "name": "init"}
        self.node_a = self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        ).data["report"][0]["jid"]

        self.assert_obj()

        payload = {"op": "global_sentinel_set"}
        self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        payload = {"op": "sentinel_active_global"}
        self.admin_client.post(
            reverse(f'jac_api:{payload["op"]}'), payload, format="json"
        )

        # Simulate celery.backend_cleanup
        PeriodicTask.objects.create(
            name="celery.backend_cleanup",
            task="celery.backend_cleanup",
            crontab=CrontabSchedule.objects.get_or_create(
                minute="0", hour="4", day_of_week="*"
            )[0],
        )

    @skip_without_redis
    def test_add_scheduled_walker(self):
        res = self.admin_client.post(
            reverse(f'jac_api:{"add_scheduled_walker"}'),
            {
                "name": "scheduled_walker",
                "schedule": {"type": "interval", "every": 1, "period": "minutes"},
                "body": {"wlk": "scheduled_walker"},
            },
            format="json",
        ).data

        self.assertEqual("Scheduled Walker created successfully!", res)

        periodic_task = PeriodicTask.objects.get(name="scheduled_walker")
        self.assertIsNotNone(periodic_task)
        self.assertEqual("scheduled_walker", periodic_task.name)

        # running the actual periodic task
        args = {
            "args": loads(periodic_task.args),
            "kwargs": loads(periodic_task.kwargs),
            "periodic_task_name": periodic_task.name,
        }

        if periodic_task.queue:
            args["queue"] = periodic_task.queue

        task_svc = JsOrc.svc("task")
        task_result = (
            task_svc.app.tasks.get(periodic_task.task).apply_async(**args).result
        )

        self.assertTrue(task_result["success"])
        self.assertEqual([True], task_result["report"])
        self.assert_obj(True)

        res = self.admin_client.post(
            reverse(f'jac_api:{"get_scheduled_queues"}'),
            {},
            format="json",
        ).data

        self.assertEqual(
            res,
            [
                {
                    "id": 2,
                    "name": "scheduled_walker",
                    "schedule": {
                        "type": "interval",
                        "conf": {"every": 1, "period": "minutes"},
                    },
                    "kwargs": {"wlk": "scheduled_walker", "mst": self.admin_master.jid},
                }
            ],
        )

        res = self.admin_client.post(
            reverse(f'jac_api:{"delete_scheduled_queue"}'),
            {"scheduled_queue_id": periodic_task.id},
            format="json",
        ).data

        self.assertEqual("Successfully deleted!", res)

    @skip_without_redis
    def test_add_scheduled_sequence(self):
        res = self.admin_client.post(
            reverse(f'jac_api:{"add_scheduled_sequence"}'),
            {
                "name": "scheduled_sequence",
                "schedule": {"type": "interval", "every": 1, "period": "minutes"},
                "body": {
                    "persistence": {
                        "additional_field": "can_be_call_via_#.additional_field",
                        "master": f"{self.admin_master.jid}",
                    },
                    "requests": [
                        {
                            "method": "JAC",
                            "api": "master_allusers",
                            "master": "{{#.master}}",
                            "body": {"limit": 0, "offset": 0},
                            "ignore_error": True,
                            "__def_loop__": {
                                "by": "$.data",
                                "filter": [
                                    {
                                        "or": [
                                            {
                                                "by": "$.user",
                                                "condition": {
                                                    "eq": "user@jaseci.com",
                                                    "ne": None,
                                                    "gt": None,
                                                    "gte": None,
                                                    "lt": None,
                                                    "lte": None,
                                                    "regex": None,
                                                },
                                            },
                                            {
                                                "and": [
                                                    {
                                                        "by": "$.user",
                                                        "condition": {
                                                            "eq": "user@jaseci.com"
                                                        },
                                                    }
                                                ]
                                            },
                                        ]
                                    }
                                ],
                                "requests": [
                                    {
                                        "method": "JAC",
                                        "api": "object_get",
                                        "master": "{{#.master}}",
                                        "body": {
                                            "obj": "{{$.jid}}",
                                            "depth": 0,
                                            "detailed": True,
                                        },
                                        "header": {
                                            "Authorization": "token {{#.login.token}}"
                                        },
                                        "ignore_error": True,
                                        "save_to": "object_get_{{!}}",
                                    },
                                    {
                                        "method": "JAC",
                                        "api": "walker_run",
                                        "master": "{{#.master}}",
                                        "body": {
                                            "name": "scheduled_sequence",
                                            "ctx": {},
                                            "nd": "{{$.active_gph_id}}",
                                            "snt": "active:sentinel",
                                        },
                                        "header": {
                                            "Authorization": "token {{#.login.token}}"
                                        },
                                        "save_to": "response_{{@.jid}}",
                                        "save_req_to": "req_{{@.jid}}",
                                    },
                                ],
                            },
                        },
                        {
                            "method": "GET",
                            "api": "https://jsonplaceholder.typicode.com/todos/100",
                            "save_to": "testing_nested",
                            "save_req_to": "req_testing_nested",
                        },
                        {
                            "method": "JAC",
                            "api": "master_allusers",
                            "master": "{{#.master}}",
                            "body": {"limit": 0, "offset": 0},
                            "save_to": "all_users",
                        },
                    ],
                },
            },
            format="json",
        ).data

        self.assertEqual("Scheduled Sequence created successfully!", res)

        periodic_task = PeriodicTask.objects.get(name="scheduled_sequence")
        self.assertIsNotNone(periodic_task)
        self.assertEqual("scheduled_sequence", periodic_task.name)

        # running the actual periodic task
        args = {
            "args": loads(periodic_task.args),
            "kwargs": loads(periodic_task.kwargs),
            "periodic_task_name": periodic_task.name,
        }

        if periodic_task.queue:
            args["queue"] = periodic_task.queue

        task_svc = JsOrc.svc("task")
        task_result = (
            task_svc.app.tasks.get(periodic_task.task).apply_async(**args).result
        )

        self.assertEqual(
            "can_be_call_via_#.additional_field", task_result["additional_field"]
        )
        self.assertEqual(self.admin_master.jid, task_result["master"])
        self.assertEqual("user@jaseci.com", task_result["object_get_0"]["name"])
        self.assertEqual("Jaseci Master", task_result["object_get_0"]["kind"])
        self.assertEqual(self.user_master.jid, task_result["object_get_0"]["jid"])

        key = sub(r"[\:\-]", "_", self.user_master.jid)

        self.assertTrue((f"req_{key}") in task_result)
        self.assertFalse(task_result[f"response_{key}"]["report"][0])
        self.assertTrue("req_testing_nested" in task_result)
        self.assertTrue("testing_nested" in task_result)
        self.assertEqual("user@jaseci.com", task_result["all_users"]["data"][0]["user"])
        self.assertEqual(
            "admin@jaseci.com", task_result["all_users"]["data"][1]["user"]
        )
        self.assert_obj(False)

    @skip_without_redis
    def test_add_scheduled_sequence_via_user(self):
        res = self.user_client.post(
            reverse(f'jac_api:{"add_scheduled_sequence"}'),
            {
                "name": "scheduled_sequence",
                "schedule": {"type": "interval", "every": 1, "period": "minutes"},
                "body": {
                    "persistence": {
                        "additional_field": "can_be_call_via_#.additional_field",
                        "master": f"{self.admin_master.jid}",
                    },
                    "requests": [],
                },
            },
            format="json",
        ).data

        self.assertEqual(
            "You do not have permission to perform this action.", str(res["detail"])
        )
