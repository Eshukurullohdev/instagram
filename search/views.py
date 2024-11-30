from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from authentication.models import User

class SearchPage(ListView):
    model = User
    template_name = 'index.html'
    context_object_name = 'users'

    def get_queryset(self):        
        queryset = super().get_queryset()
        ism = self.request.GET.get("ism")
        if ism:
            queryset = queryset.filter(fullName__icontains=ism)
        return queryset
