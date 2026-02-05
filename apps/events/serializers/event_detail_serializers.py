from rest_framework import serializers

from events.models.event import Event

from events.serializers.event_activity_serializers import EventActivityDetailSerializers
from events.serializers.attendance_serializers import AttendanceSerializer


class EventDetailSerializer(serializers.ModelSerializer):
    event_activities = EventActivityDetailSerializers(source = "eventactivity_set",many=True, read_only=True)
    event_participants = AttendanceSerializer( source="eventattendant_set",many=True, read_only=True)

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
        ]
        read_only_fields = ["id", "created_by"]