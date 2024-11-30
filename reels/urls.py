from django.urls import path
from .views import ReelsView

urlpatterns = [
    path("<str:unique_id>/", ReelsView.as_view(), name="reel")
]

"""
Bu  urls reels uchun ishlayapti
"""
