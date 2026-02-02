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
    
    def create(self, validated_data):
        weekday_data = validated_data.pop('weekday', [])
        availability_rule = AvailabilityRule.objects.create(**validated_data)
        
        # Create RuleWeekday entries
        for day in weekday_data:
            RuleWeekday.objects.create(rule_id=availability_rule.id, weekday=day)
        
        return availability_rule
    
    def update(self, instance, validated_data):
        weekday_data = validated_data.pop('weekday', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if weekday_data is not None:
            # Clear existing weekdays
            RuleWeekday.objects.filter(rule_id=instance.id).delete()
            # Create new RuleWeekday entries
            for day in weekday_data:
                RuleWeekday.objects.create(rule_id=instance.id, weekday=day)
        
        return instance
    
    def delete(self, instance):
        # Delete associated RuleWeekday entries
        RuleWeekday.objects.filter(rule_id=instance).delete()
        # Delete the AvailabilityRule instance
        instance.delete()
        

    def get_rule_weekdays(self, obj):
        return list(obj.rule_weekdays.values_list('weekday', flat=True))