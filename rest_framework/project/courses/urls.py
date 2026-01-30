from django.urls import path
from .views import CourseListCreateAPIView, CourseDetailAPIView

urlpatterns = [
    path('courses/', CourseListCreateAPIView.as_view(), name='courses-list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='courses-detail'),
]
