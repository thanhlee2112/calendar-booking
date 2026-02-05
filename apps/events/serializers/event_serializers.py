from rest_framework import serializers
from events.models.event import Event


class EventSerializer(serializers.ModelSerializer):
    activities = serializers.ListField(
    child = serializers.IntegerField(min_value=0, max_value=6),
    write_only = True,
    )
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'created_by', 'activities', 'eligible_notification', 'ineligible_notification']
        read_only_fields = ['id']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data