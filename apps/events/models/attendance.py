from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
class EventAttendant(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attended_at = models.DateTimeField(auto_now_add=True)
