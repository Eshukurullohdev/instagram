from django.urls import path

from . import views


urlpatterns = [
    path("add-like/<int:post_id>/", views.add_like, name="add_like"),
    path("add-like-reels/<int:reel_id>/", views.add_like_reels, name="add_like_reels"),
]