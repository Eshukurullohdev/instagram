from django.contrib import admin
from .models import Story, ExtendedStory

admin.site.register(Story)
admin.site.register(ExtendedStory)
