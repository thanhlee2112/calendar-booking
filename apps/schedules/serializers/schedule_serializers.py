from rest_framework import serializers
from schedules.models.schedules import Schedule
from common.utils.hashid import encode_id

class ScheduleSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Schedule
        fields = [
            'id',
            'created_by',
            'name',
            'description',
            'start_time',
            'end_time',
        ]
        read_only_fields = ['id']
        unique_together = ['created_by', 'start_time', 'end_time']
    def get_id(self, obj):
        return encode_id(obj.id)