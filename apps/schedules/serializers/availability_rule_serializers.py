from rest_framework import serializers
from schedules.models.availability_rule import AvailabilityRule
from schedules.models.rule_weekday import RuleWeekday


class AvailabilityRuleSerializer(serializers.ModelSerializer):
    weekday = serializers.ListField(
        child = serializers.IntegerField(min_value=0, max_value=6),
        write_only = True,
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    rule_weekdays = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AvailabilityRule
        fields = [
            'id',
            'user',
            'start_time',
            'rule_weekdays',
            'weekday',
            'end_time',
            'valid_from',
            'valid_to',
        ]

        read_only_fields = ['id']
    
    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data
            

    def get_rule_weekdays(self, obj):
        return list(obj.rule_weekdays.values_list('weekday', flat=True))