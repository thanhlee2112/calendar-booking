from django.db import models

class RuleWeekday(models.Model):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    WEEKDAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]

    rule = models.ForeignKey('schedules.AvailabilityRule', related_name='rule_weekdays', on_delete=models.CASCADE)
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)

    def __str__(self):
        return self.get_weekday_display()
    
    class Meta:
        unique_together = ('rule_id', 'weekday')
        ordering = ['rule_id']