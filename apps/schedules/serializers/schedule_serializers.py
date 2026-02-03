from rest_framework import serializers
from schedules.models.schedules import Schedule

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