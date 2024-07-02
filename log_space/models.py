from django.db import models
from django.utils import timezone


class APILog(models.Model):
    username = models.CharField(max_length=150)
    date_time = models.DateTimeField(default=timezone.now)
