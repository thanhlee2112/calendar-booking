from django.db import transaction
from django.db.models import Q, Count, Prefetch
from rest_framework.exceptions import NotFound
from django.conf import settings

from django.core.exceptions import ValidationError

from events.models.event_activities import EventActivity
from events.models.attendance import EventAttendant
from events.models.event import Event
from schedules.models.availability_rule import AvailabilityRule
from schedules.models.schedules import Schedule

class AttendanceService():
    
    def create(self, user, validated_data):
        try:
            print(validated_data['event'])
            if self.is_eligible_for_attendance(user, validated_data['event']):
                validated_data.pop('user', None)
                event = Event.objects.get(id=validated_data['event'])
                event_attendant = EventAttendant.objects.create(user=user, event=event)
            else:
                raise ValidationError("You are not eligible to attend this event.")
            return event_attendant
        except ValidationError as e:
            raise ValidationError(e.message)
    
    def is_eligible_for_attendance(self, user, event_id):
        try:
            event = Event.objects.get(id=event_id)
            is_available = AvailabilityRule.objects.filter(user=user, rule_weekdays__weekday=(event.start_time).weekday(), start_time__lte=event.start_time.time(), end_time__gte=event.start_time.time()).exists()
            is_overlap_schedule = Schedule.objects.filter(Q(start_time__lt=event.end_time, end_time__gt=event.start_time)).exists()
            return not is_available and not is_overlap_schedule
        except Event.DoesNotExist:
            return False