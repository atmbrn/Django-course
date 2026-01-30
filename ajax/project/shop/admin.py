from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes', 'dislikes', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'post', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('text', 'post__title')
    ordering = ('-created_at',)
