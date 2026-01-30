from django.urls import path

from . import views

urlpatterns = [
    path("posts/", views.posts_list, name="posts"),
    path("posts/comment/add/", views.add_comment, name="add_comment"),
    path("posts/comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("posts/<int:post_id>/like/", views.like_post, name="like_post"),
    path("posts/<int:post_id>/dislike/", views.dislike_post, name="dislike_post"),
]
