import logging

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import Signal, receiver

from .models import Topic, TopicActivity

logger = logging.getLogger(__name__)

# custom signal
topic_changed = Signal()


@receiver(m2m_changed, sender=Topic.subscribers.through)
def handle_subscribers_changed(sender, instance, action, pk_set, **kwargs):
    """Invalidate cache when subscribers change."""
    if action in ("post_add", "post_remove"):
        # pk_set are user ids added/removed
        user_ids = pk_set or set()
        for uid in user_ids:
            cache.delete(f"user:{uid}:topics")
    elif action == "post_clear":
        # best-effort: clear cache for all users
        from django.contrib.auth import get_user_model

        User = get_user_model()
        for user in User.objects.all():
            cache.delete(f"user:{user.id}:topics")


@receiver(post_save, sender=Topic)
def handle_topic_saved(sender, instance, created, **kwargs):
    if created:
        TopicActivity.objects.create(topic=instance, action=TopicActivity.ACTION_CREATED)
        topic_changed.send(sender=sender, topic_id=instance.id, action=TopicActivity.ACTION_CREATED)
    else:
        # record update activity and emit signal
        TopicActivity.objects.create(topic=instance, action=TopicActivity.ACTION_UPDATED)
        topic_changed.send(sender=sender, topic_id=instance.id, action=TopicActivity.ACTION_UPDATED)


@receiver(post_delete, sender=Topic)
def handle_topic_deleted(sender, instance, **kwargs):
    TopicActivity.objects.create(topic=instance, action=TopicActivity.ACTION_DELETED)
    topic_changed.send(sender=sender, topic_id=instance.id, action=TopicActivity.ACTION_DELETED)


# handler for our custom signal - connected explicitly in apps.ready
def handle_topic_changed(sender, topic_id, action, **kwargs):
    logger.info(f"Topic {topic_id} changed: {action}")

    # try to invalidate cache for users subscribed to this topic
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        # topic deleted - best-effort: clear cache for all users
        from django.contrib.auth import get_user_model

        User = get_user_model()
        for user in User.objects.all():
            cache.delete(f"user:{user.id}:topics")
        return

    for user in topic.subscribers.all():
        cache.delete(f"user:{user.id}:topics")
