from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from kash.user.models import User


@override_settings(TESTING=True, CELERY_TASK_ALWAYS_EAGER=True)
class AuthTestCase(APITestCase):
    def test_register(self):
        response = self.client.post(
            reverse("auth-register"),
            data={
                "name": "Test User",
                "kashtag": "testuser",
                "password": "testuser",
                "confirm": "testuser",
                "referral_code": "test",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("refresh"))
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(response.data.get("user"))
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login(self):
        user = User.objects.create(username="testlogin")
        user.set_password("testlogin")
        user.save()
        response = self.client.post(
            reverse("auth-login"),
            data={
                "username": user.username,
                "password": "testlogin",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("refresh"))
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(response.data.get("user"))
        self.assertIsNotNone(response.data.get("user").get("id"), user.pk)
