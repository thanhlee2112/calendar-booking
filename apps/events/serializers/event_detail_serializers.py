from rest_framework import serializers

from events.models.event import Event

from django.db.models import Q

from events.serializers.event_activity_serializers import EventActivityDetailSerializers
from events.serializers.attendance_serializers import AttendanceSerializer
# Kiểm availability_rule
from schedules.models.availability_rule import AvailabilityRule
from schedules.models.rule_weekday import RuleWeekday

class EventDetailSerializer(serializers.ModelSerializer):
    event_activities = EventActivityDetailSerializers(source = "eventactivity_set",many=True, read_only=True)
    event_participants = AttendanceSerializer( source="eventattendant_set",many=True, read_only=True)
    is_eligible = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_time",
            "end_time",
            "created_by",
            "event_activities",
            "event_participants",
            "is_eligible",
        ]
        read_only_fields = ["id", "created_by"]

    def get_is_eligible(self, obj):
        user = self.context['request'].user
        event_start = obj.start_time
        event_end = obj.end_time
        weekday = event_start.weekday()  # Nếu RuleWeekday dùng 1-7

        ar_overlap = AvailabilityRule.objects.filter(
            user=user,
            rule_weekdays__weekday=weekday,
            start_time__lte=event_start.time(),
            end_time__gt=event_start.time(),
        ).filter(
            Q(valid_from__isnull=True) | Q(valid_from__lte=event_start),
            Q(valid_to__isnull=True) | Q(valid_to__gte=event_start)
        ).exists()

        # Kiểm schedule
        from schedules.models.schedules import Schedule
        schedule_overlap = Schedule.objects.filter(
            created_by=user,
            start_time__lt=event_end,
            end_time__gt=event_start
        ).exists()

        return not (ar_overlap or schedule_overlap)