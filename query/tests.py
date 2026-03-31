from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthDashboardTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="TestPass123!",
            first_name="Aziz",
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tetratex Dashboard")

    def test_home_redirects_for_anonymous_user(self):
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")

    def test_user_can_login_and_open_dashboard(self):
        logged_in = self.client.login(username="testuser", password="TestPass123!")
        self.assertTrue(logged_in)

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Xush kelibsiz, Aziz")
