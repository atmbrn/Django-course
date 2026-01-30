from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordChangeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="old_password")
        self.client.login(username="testuser", password="old_password")

    def test_password_change(self):
        resp = self.client.post(
            reverse("password_change"),
            {
                "old_password": "old_password",
                "new_password1": "newsecurepassword",
                "new_password2": "newsecurepassword",
            },
            follow=True,
        )
        self.assertRedirects(resp, reverse("password_change_done"))
        self.assertTrue("_auth_user_id" in self.client.session)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepassword"))
        self.assertFalse(self.user.check_password("old_password"))
