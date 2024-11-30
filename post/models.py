from django.db import models
from authentication.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    image = models.ImageField()
    text = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.user.username + " post joyladi"    
