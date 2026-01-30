from django.apps import AppConfig


class TopicsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "topics"

    def ready(self):
        # import signals so decorators/receivers are registered
        from . import signals
        # connect custom signal handler explicitly as required by the homework
        signals.topic_changed.connect(signals.handle_topic_changed)
