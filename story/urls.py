from django.urls import path
from . import views

urlpatterns = [
    path('detail/<str:username>/', views.SingleStoryView.as_view(), name="story_detail"),
    path("create-story/", views.CreateStoryView.as_view()),
    path("create-story/create-with-resource/", views.CreateStoryWithResource.as_view(), name='create_story_with_image'),
]