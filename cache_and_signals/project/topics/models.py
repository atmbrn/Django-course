from django.conf import settings
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="topics", blank=True)

    def __str__(self):
        return self.name


class TopicActivity(models.Model):
    ACTION_CREATED = "created"
    ACTION_DELETED = "deleted"
    ACTION_UPDATED = "updated"

    ACTION_CHOICES = [
        (ACTION_CREATED, "created"),
        (ACTION_DELETED, "deleted"),
        (ACTION_UPDATED, "updated"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="activities")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TopicActivity(topic={self.topic_id}, action={self.action})"
