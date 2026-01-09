from django.contrib import admin

from .models import Topic, TopicActivity


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(TopicActivity)
class TopicActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "action", "created_at")
    list_filter = ("action",)
