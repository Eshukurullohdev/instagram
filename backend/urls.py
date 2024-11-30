
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("instagram.urls")),
    path("authentication/", include("authentication.urls")),
    path("search/", include("search.urls")),
    path("story/", include("story.urls")),
    path("reels/", include("reels.urls")),
    path("like/", include("like.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
