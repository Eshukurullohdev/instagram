from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from authentication.models import User
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from story.models import Story
from django.db.models import Q
from subscription.models import Subscription
from post.models import Post
from like.models import PostLike

class HomePage(ListView):
    model = Story
    template_name = "main.html"
    context_object_name = 'stories'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/authentication/login/")
        elif not request.user.step_completed:
            return redirect("/authentication/step/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        joriy_user = self.request.user
        dost = Subscription.objects.filter(
            Q(user=joriy_user) |
            Q(to=joriy_user)
        )
        queryset = queryset.filter(
            Q(user__in=dost.values_list('to', flat=True)) | 
            Q(user__in=dost.values_list('user', flat=True)) | 
            Q(user=joriy_user)).order_by('-date_created')
        queryset = queryset.exclude(user=joriy_user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['my_story'] = Story.objects.get(user=self.request.user)
        except Story.DoesNotExist:
            pass
        is_liked = []
        posts = Post.objects.all().order_by('-date_created')
        
        for post in posts:
            try:
                PostLike.objects.get(post=post, user=self.request.user)
                is_liked.append(True)
            except PostLike.DoesNotExist:
                is_liked.append(False)
        context['is_liked'] = is_liked
        context['posts'] = zip(posts, is_liked)
        # (karimni-posti, True)
        # (Halimani-posti, False)
        # (Jamshid-post, False)
        return context
    
    






