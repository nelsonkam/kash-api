from http.client import METHOD_NOT_ALLOWED, OK

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from kash.user.models import User, UserProfile


class ProfileViewsetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user, _ = User.objects.get_or_create(username="test", phone_number="00000000")
        cls.user = user
        cls.profile = UserProfile.objects.create(user=cls.user, kashtag="test")

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.user)

    def test_create_profile_fail(self):
        # Users should not be able to create a profile
        # using POST /profile/
        response = self.client.post(
            reverse("profiles-list"),
        )
        self.assertEqual(response.status_code, METHOD_NOT_ALLOWED)

    def test_get_current_user(self):
        response = self.client.get(
            reverse("profiles-detail", kwargs={"pk": 'current'}),
        )
        self.assertEqual(response.status_code, OK)
        self.profile.refresh_from_db()
        self.assertEqual(response.data, {
            'name': self.profile.name,
            'phone_number': self.profile.phone_number,
            "kashtag": self.profile.kashtag,
            "avatar_url": self.profile.avatar_url,
            "device_ids": self.profile.device_ids,
            "referral_code": self.profile.referral_code,
            "promo_balance": self.profile.promo_balance,
        })

    def test_add_device_id(self):
        device_id = 'random-device-id'
        response = self.client.post(
            reverse("profiles-device-ids", kwargs={"pk": 'current'}),
            data={'device_id': device_id}
        )
        self.assertEqual(response.status_code, OK)
        self.profile.refresh_from_db()
        self.assertIn(device_id, self.profile.device_ids)


