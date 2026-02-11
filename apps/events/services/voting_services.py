from django.db import transaction
from django.db.models import Q, Count, Prefetch
from rest_framework.exceptions import NotFound
from django.conf import settings

from django.core.exceptions import ValidationError

from events.models.event_activities import EventActivity
from events.models.event_activities_voting import EventActivityVoting
from schedules.models.availability_rule import AvailabilityRule
from schedules.models.schedules import Schedule

class VotingService():
    def vote(self, user, event_activity_voting):
        try:
            print(event_activity_voting)
            if isinstance(event_activity_voting['activity'], int):
                event_activity = EventActivity.objects.get(id=event_activity_voting['activity'])
                if event_activity and self.is_eligible_for_voting(user, event_activity):
                    event_activity = EventActivityVoting.objects.create(voted_by=user, event_activity=event_activity, is_eligible=True)
                    return "Voted successfully."
            else:
                for activity in event_activity_voting['activity']:
                    event_activity = EventActivity.objects.get(id=activity)
                    if event_activity and self.is_eligible_for_voting(user, event_activity):
                        EventActivityVoting.objects.create(voted_by=user, event_activity=event_activity, is_eligible=True)
                    return "Voted successfully."
                else:
                    raise ValidationError("You are not eligible to vote for this activity.")
        except EventActivity.DoesNotExist:
            raise NotFound("Event activity not found.")
        except ValidationError as e:
            raise ValidationError(e.message)

    def is_eligible_for_voting(self, user, event_activity):
        event = event_activity.event
        is_available = AvailabilityRule.objects.filter(user=user, rule_weekdays__weekday=(event.start_time).weekday(), start_time__lte=event.start_time.time(), end_time__gte=event.start_time.time()).exists()
        is_overlap_schedule = Schedule.objects.filter(Q(start_time__lt=event.end_time, end_time__gt=event.start_time)).exists()
        return not is_available and not is_overlap_schedule
    
    def remove_vote(self, user, event_activity_id):
        try:
            vote = EventActivityVoting.objects.get(voted_by=user, event_activity_id=event_activity_id)
            vote.delete()
            return {"detail": "Vote removed successfully."}
        except EventActivityVoting.DoesNotExist:
            raise NotFound("Vote not found.")