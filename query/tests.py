from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginRememberMeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="secret123"
        )

    def test_login_without_remember_me_sets_session_cookie_expiry(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "secret123"},
        )

        self.assertRedirects(response, reverse("farmer_report"))
        self.assertEqual(self.client.session.get_expiry_age(), 0)

    def test_login_with_remember_me_sets_14_day_expiry(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "secret123",
                "rememberme": "on",
            },
        )

        self.assertRedirects(response, reverse("farmer_report"))
        self.assertEqual(self.client.session.get_expiry_age(), 60 * 60 * 24 * 14)
