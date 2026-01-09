from django.test import TestCase, Client
from django.urls import reverse


class VisitCounterTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_visit_counter_increments(self):
        resp = self.client.get(reverse("visit_counter"))
        self.assertContains(resp, "You have visited this page 1 times")
        resp = self.client.get(reverse("visit_counter"))
        self.assertContains(resp, "You have visited this page 2 times")

    def test_reset_visit_counter(self):
        self.client.get(reverse("visit_counter"))
        resp = self.client.get(reverse("reset_visit_counter"))
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse("visit_counter"))
        self.assertContains(resp, "You have visited this page 1 times")
