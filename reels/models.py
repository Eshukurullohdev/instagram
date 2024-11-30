from django.db import models
from authentication.models import User
from story.validator import validate_file_video

from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator

"""
Reels model
1.User
2.Video
3.description
4.date Created
"""

class Reel(models.Model):
    unique_id = models.CharField(
        max_length=90,
        validators=[
            RegexValidator(
                regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*])[^?&^]{-}$",
                message="Bu symbollardan tashqari ?&^",
                code="hato_boldi",
            )
        ],
        unique=True,  # yagona bo'lishi uchun
        null=True,
        blank=True,
        help_text="Bu yerda faqat 12ta lik random string, number va symboldan iborat bo'ladi va siz buni yaratishiz shart emas, dastur o'zi yaratib beradi",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reel")
    video = models.FileField(upload_to="reel/", validators=[validate_file_video])
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)  
    
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = get_random_string(
                length=12,
                allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            )
        super().save(*args, **kwargs)  
    
    def __str__(self):
        return f"{self.user} - Reels yaratdi. {self.description}"
