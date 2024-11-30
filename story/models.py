from django.db import models
from authentication.models import User
from .validator import validate_file_extension
from django.utils import timezone

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="story")
    resource = models.FileField(upload_to="story/", validators=[validate_file_extension])
    is_valid = models.BooleanField(default=True)
    text = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def qolgan_vaqtni_topish(self):
        hozir = timezone.now()
        qolgan_vaqt = hozir.hour - self.date_created.hour
        if qolgan_vaqt <= 0:
            return "Now"
        return "%sh" % qolgan_vaqt
    
    def __str__(self):
        return "%s - %sda qo'yilgan story" % (self.user.fullName, self.date_created)

class ExtendedStory(models.Model):
    story = models.ForeignKey(Story, on_delete=models.SET_NULL, null=True, related_name="extended")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="extended_story")
    resource = models.FileField(upload_to="story/", validators=[validate_file_extension])
    text = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return "%s - %sda qo'yilgan story" % (self.user.fullName, self.date_created)