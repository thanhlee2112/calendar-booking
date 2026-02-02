from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

class EventActivityVoting(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    activity = models.ForeignKey('activities.Activity', on_delete=models.CASCADE)
    vote_number = models.IntegerField();
    voted_at = models.DateTimeField(auto_now_add=True)