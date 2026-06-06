from rest_framework import serializers
from schedules.models.schedules import Schedule
from common.utils.hashid import encode_id

class ScheduleSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    username = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Schedule
        fields = [
            'id',
            'created_by',
            'name',
            'username',
            'description',
            'start_time',
            'end_time',
        ]
        read_only_fields = ['id']
        unique_together = ['created_by', 'start_time', 'end_time']
    def get_id(self, obj):
        return encode_id(obj.id)
    def get_username(self, obj):
        return obj.created_by.username if obj.created_by else None