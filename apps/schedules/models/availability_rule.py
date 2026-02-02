from django.db import models
from django.conf import settings

class AvailabilityRule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    valid_from = models.DateField(null=True)
    valid_to = models.DateField(null=True)

    class Meta:
        unique_together = ('user', 'start_time', 'end_time', 'valid_from', 'valid_to')
        ordering = ['start_time']
