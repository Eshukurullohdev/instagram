from django.shortcuts import render, redirect
from .models import *
from post.models import Post
from reels.models import Reel

def add_like(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
        try:
            like = PostLike.objects.get(post=post, user=request.user)
            like.delete()
        except PostLike.DoesNotExist:
            PostLike.objects.create(post=post, user=request.user)
        return redirect("/")
    return redirect("/authentication/login/")

def add_like_reels(request, reel_id):
    if request.user.is_authenticated:
        reel = Reel.objects.get(id=reel_id)
        first_reel = Reel.objects.first()
        try:
            like = ReelsLike.objects.get(reel=reel, user=request.user)
            like.delete()
        except ReelsLike.DoesNotExist:
            ReelsLike.objects.create(reel=reel, user=request.user)
        return redirect("/reels/")
    return redirect("/authentication/login/")
