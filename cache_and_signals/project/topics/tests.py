from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from .models import Topic, TopicActivity


class TopicsSignalsAndCacheTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="testuser", password="pass")
        self.client = Client()
        self.client.force_login(self.user)
        # ensure topics exist
        Topic.objects.get_or_create(name="Python")
        Topic.objects.get_or_create(name="Django")
        Topic.objects.get_or_create(name="DevOps")

    def test_subscribe_invalidates_cache(self):
        key = f"user:{self.user.id}:topics"
        # prime cache
        resp = self.client.get("/topics/")
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(cache.get(key))

        topic = Topic.objects.first()
        # subscribe
        resp = self.client.post(f"/topics/subscribe/{topic.id}/")
        self.assertEqual(resp.status_code, 302)

        # m2m_changed signal should have cleared cache for this user
        self.assertIsNone(cache.get(key))

    def test_create_generates_activity_and_sends_signal(self):
        t = Topic.objects.create(name="NewTopic")
        self.assertTrue(TopicActivity.objects.filter(topic=t, action=TopicActivity.ACTION_CREATED).exists())

    def test_delete_generates_activity(self):
        t = Topic.objects.create(name="ToDelete")
        t_id = t.id
        t.delete()
        self.assertTrue(TopicActivity.objects.filter(topic_id=t_id, action=TopicActivity.ACTION_DELETED).exists())
