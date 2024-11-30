from django.db import models
from authentication.models import User

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subsciption_from")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subsciption_to")
    send_time = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)
    accept = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user} - {self.to}ga do'stlik so'rovini yubordi. Holati: {'Kutilmoqda' if self.state else 'Yakunlandi' ' Dostlik Qabul qilindi' if self.accept else ''}"
