from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    support_send = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "message of" + self.user.first_name + " " + self.user.last_name
