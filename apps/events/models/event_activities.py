from django.db import models
from django.conf import settings

class EventActivity(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    activity = models.ForeignKey('activities.Activity', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)