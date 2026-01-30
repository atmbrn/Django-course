from django.urls import path

from . import views

app_name = "topics"

urlpatterns = [
    path("", views.topics_view, name="list"),
    path("subscribe/<int:id>/", views.subscribe_view, name="subscribe"),
    path("unsubscribe/<int:id>/", views.unsubscribe_view, name="unsubscribe"),
    path("create/", views.create_topic_view, name="create"),
    path("delete/<int:id>/", views.delete_topic_view, name="delete"),
]
