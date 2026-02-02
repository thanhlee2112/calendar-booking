from rest_framework import serializers
from events.models.event import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'created_by']
        read_only_fields = ['id']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data