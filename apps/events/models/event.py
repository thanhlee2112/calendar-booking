from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    eligible_notification = models.TextField(blank=True, null=True)
    ineligible_notification = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['start_time', 'end_time']