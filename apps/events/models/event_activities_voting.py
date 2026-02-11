from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

class EventActivityVoting(models.Model):
    event_activity = models.ForeignKey('events.EventActivity', on_delete=models.CASCADE,related_name='votes')
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)
    is_eligible = models.BooleanField(default=True)
