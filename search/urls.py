from django.urls import path
from .views import *

urlpatterns = [
    path('', SearchPage.as_view(), name='search'),
]