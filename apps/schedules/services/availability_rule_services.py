from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ValidationError

from schedules.models.availability_rule import AvailabilityRule
from schedules.models.rule_weekday import RuleWeekday

class AvailabilityRuleService:

    def create(self , user, validated_data):
        weekday_data = validated_data.pop('weekday', [])
        is_valid = self.valid_no_overlap(user=user, start_time=validated_data['start_time'], 
                                 end_time=validated_data['end_time'],
                                 valid_from=validated_data.get('valid_from'), 
                                 weekdays=weekday_data)
        if is_valid:
            availability_rule = AvailabilityRule.objects.create(**validated_data)

            RuleWeekday.objects.bulk_create([
                RuleWeekday(rule_id=availability_rule.id, weekday=day) for day in weekday_data
            ])
            return availability_rule
        else:
            raise ValidationError("The availability rule overlaps with existing rules.")
    
    def update(self, instance, validated_data):
        weekday_data = validated_data.pop('weekday', None)
        
        conflict_exists = AvailabilityRule.objects.filter(
            user = instance.user,
            rule_weekdays__weekday__in=weekday_data,
            start_time__lt=validated_data['end_time'],
            end_time__gt=validated_data['start_time'],
            valid_from__lte=validated_data['valid_from'],
            valid_to__gte=validated_data['valid_from'],
        ).exclude(id=instance.id).exists()
        
        if conflict_exists:
            raise ValidationError("The updated availability rule overlaps with existing rules.")
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
    
    @staticmethod
    def valid_no_overlap(*, user, start_time, end_time, valid_from=None, weekdays):
        qs = AvailabilityRule.objects.filter(
            user=user,
            rule_weekdays__weekday__in=weekdays,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        if(valid_from is not None):
            qs = qs.filter(
                valid_from__lte=valid_from,
                valid_to__gt=valid_from,
            )
        return not qs.exists()