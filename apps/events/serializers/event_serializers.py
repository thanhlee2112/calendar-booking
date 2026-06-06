from rest_framework import serializers
from events.models.event import Event


class EventSerializer(serializers.ModelSerializer):
    activities = serializers.ListField(
    child = serializers.IntegerField(min_value=0, max_value=6),
    write_only = True,
    )
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'created_by','user', 'activities', 'eligible_notification', 'ineligible_notification', 'creator_channel_id']
        read_only_fields = ['id']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data
    def get_user(self, obj):
        return obj.created_by.username if obj.created_by else None