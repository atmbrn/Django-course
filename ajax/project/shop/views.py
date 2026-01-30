from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .models import Post, Comment


def posts_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    return render(
        request,
        template_name="shop/posts.html",
        context={"posts": posts},
    )


@require_http_methods(["POST"])
def add_comment(request: HttpRequest) -> JsonResponse:
    post_id = request.POST.get("post_id")
    text = request.POST.get("text", "").strip()

    if not text:
        return JsonResponse({"error": "Comment text cannot be empty"}, status=400)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    comment = Comment.objects.create(post=post, text=text)

    return JsonResponse({
        "id": comment.id,
        "text": comment.text,
        "comments_count": post.comment_set.count(),
    })


@require_http_methods(["POST"])
def delete_comment(request: HttpRequest, comment_id: int) -> JsonResponse:
    try:
        comment = Comment.objects.get(id=comment_id)
        post = comment.post
        comment.delete()
        return JsonResponse({
            "comments_count": post.comment_set.count(),
        })
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found"}, status=404)


@require_http_methods(["POST"])
def like_post(request: HttpRequest, post_id: int) -> JsonResponse:
    try:
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({
            "likes": post.likes,
            "dislikes": post.dislikes,
        })
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)


@require_http_methods(["POST"])
def dislike_post(request: HttpRequest, post_id: int) -> JsonResponse:
    try:
        post = Post.objects.get(id=post_id)
        post.dislikes += 1
        post.save()
        return JsonResponse({
            "likes": post.likes,
            "dislikes": post.dislikes,
        })
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
