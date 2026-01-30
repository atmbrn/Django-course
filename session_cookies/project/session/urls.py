from django.urls import path

from . import views

urlpatterns = [
    path("set-cookies/", views.set_cookies, name="set_cookies"),
    path("delete-cookies/", views.delete_cookies, name="delete_cookies"),
    path("get-cookies/", views.get_cookies, name="get_cookies"),
    path("set-session/", views.set_session, name="set_session"),
    path("get-session/", views.get_session, name="get_session"),
    path("clear-session/", views.clear_session, name="clear_session"),
    path("update-session/", views.update_session, name="update_session"),
    path("visit/", views.visit_counter, name="visit_counter"),
    path("visit/reset/", views.reset_visit_counter, name="reset_visit_counter"),
]
