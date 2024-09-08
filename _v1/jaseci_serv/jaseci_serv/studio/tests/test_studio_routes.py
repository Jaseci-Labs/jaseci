import os
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from jaseci_serv.settings import BASE_DIR


class StudioRoutesTestWithTemplates(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.override_settings = override_settings(
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "APP_DIRS": True,
                    "DIRS": [
                        os.path.join(
                            BASE_DIR, "jaseci_serv/studio/tests/mocks_templates/"
                        ),
                    ],
                }
            ]
        )
        cls.override_settings.__enter__()

    @classmethod
    def tearDownClass(cls):
        print("Tearing down class")
        cls.override_settings.__exit__(None, None, None)
        super().tearDownClass()

    def setUp(self):
        self.client = Client()

    def test_studio_index(self):
        response = self.client.get(reverse("studio_index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "studio/index.html")

    def test_studio_dashboard(self):
        response = self.client.get(reverse("studio_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "studio/dashboard.html")

    def test_studio_graph_viewer(self):
        response = self.client.get(reverse("studio_graph_viewer"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "studio/graph-viewer.html")

    def test_studio_logs(self):
        response = self.client.get(reverse("studio_logs_viewer"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "studio/logs.html")

    def test_studio_architype(self):
        response = self.client.get(reverse("studio_architype"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "studio/architype.html")

    def test_studio_actions(self):
        response = self.client.get(reverse("studio_actions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "studio/actions.html")


class StudioRoutesTestWithoutTemplates(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.override_settings = override_settings(
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "APP_DIRS": True,
                    "DIRS": [
                        os.path.join(
                            BASE_DIR,
                            "jaseci_serv/studio/tests/missing_mocks_templates/",
                        ),
                    ],
                }
            ]
        )
        cls.override_settings.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.override_settings.__exit__(None, None, None)
        super().tearDownClass()

    def setUp(self):
        self.client = Client()

    def test_studio_index(self):
        response = self.client.get(reverse("studio_index"))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Jaseci Studio is not installed.")

    def test_studio_graph_viewer(self):
        response = self.client.get(reverse("studio_graph_viewer"))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Jaseci Studio is not installed.")

    def test_studio_logs(self):
        response = self.client.get(reverse("studio_logs_viewer"))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Jaseci Studio is not installed.")

    def test_studio_architype(self):
        response = self.client.get(reverse("studio_architype"))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Jaseci Studio is not installed.")

    def test_studio_actions(self):
        response = self.client.get(reverse("studio_actions"))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Jaseci Studio is not installed.")
