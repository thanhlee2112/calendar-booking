from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ValidationError

from schedules.models.availability_rule import AvailabilityRule
from schedules.models.rule_weekday import RuleWeekday
from schedules.models.schedules import Schedule

from django.db.models.functions import TruncDate, TruncTime
class ScheduleService:

    def create(self, created_by, validated_data):
        # use the provided user for validation
        try:
            is_valid = self.validate_schedule_time(user=created_by, start_time=validated_data['start_time'], 
                                             end_time=validated_data['end_time'])
            schedule = None
            if is_valid:
                # ensure the model field name `created_by` is present on the data
                validated_data['created_by'] = created_by
                schedule = Schedule.objects.create(**validated_data)
                print(schedule)
            return schedule
        except ValidationError as e:
            raise ValidationError(e.message)
    
    def validate_schedule_time(self,user, start_time, end_time):
        if start_time >= end_time:
            raise ValidationError("Start time must be before end time.")
        if start_time.hour < 0 or end_time.hour > 24:
            raise ValidationError("Time must be within 0 to 24 hours.")
        availability_exists = AvailabilityRule.objects.filter(
            user=user,
            rule_weekdays__weekday=(start_time).weekday(),
            start_time__lte=start_time.time(),
            end_time__gte=end_time.time(),
        )
        print(availability_exists.query)
        if availability_exists.exists():
            raise ValidationError("The schedule time is overlap with your availability.")
        return True