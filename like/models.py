from django.db import models
from post.models import Post
from authentication.models import User
from reels.models import Reel

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_post")
    date_liked = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.post) + ' uchun like bosildi'
    
class ReelsLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reel_like")
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name="like_reel")
    date_liked = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.reel) + ' uchun like bosildi'
