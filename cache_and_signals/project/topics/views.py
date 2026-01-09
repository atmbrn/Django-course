from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render

from .models import Topic

CACHE_TTL = 60  # seconds


@login_required
def topics_view(request):
    key = f"user:{request.user.id}:topics"
    topics_data = cache.get(key)
    if topics_data is None:
        qs = Topic.objects.all()
        topics_data = []
        for t in qs:
            topics_data.append(
                {
                    "id": t.id,
                    "name": t.name,
                    "subscribers_count": t.subscribers.count(),
                    "is_subscribed": request.user in t.subscribers.all(),
                }
            )
        cache.set(key, topics_data, CACHE_TTL)
    return render(request, "topics/topics.html", {"topics": topics_data})


@login_required
def subscribe_view(request, id):
    if request.method != "POST":
        return redirect("topics:list")
    topic = get_object_or_404(Topic, pk=id)
    topic.subscribers.add(request.user)
    return redirect("topics:list")


@login_required
def unsubscribe_view(request, id):
    if request.method != "POST":
        return redirect("topics:list")
    topic = get_object_or_404(Topic, pk=id)
    topic.subscribers.remove(request.user)
    return redirect("topics:list")


@login_required
def create_topic_view(request):
    if request.method != "POST":
        return redirect("topics:list")
    name = request.POST.get("name")
    if name:
        Topic.objects.create(name=name)
    return redirect("topics:list")


@login_required
def delete_topic_view(request, id):
    if request.method != "POST":
        return redirect("topics:list")
    topic = get_object_or_404(Topic, pk=id)
    topic.delete()
    return redirect("topics:list")
