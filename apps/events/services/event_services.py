from django.db import transaction
from django.db.models import Q, Count, Prefetch
from rest_framework.exceptions import NotFound
from django.conf import settings

from django.core.exceptions import ValidationError

from events.models.event_activities import EventActivity
from events.models.attendance import EventAttendant
from events.models.event import Event
from schedules.models.availability_rule import AvailabilityRule
from schedules.models.schedules import Schedule
from notifications.services.discord_notification_services import DiscordNotificationService
from allauth.socialaccount.models import SocialAccount

class EventService:

    def create_event(self, user, event_data):
        with transaction.atomic():
            self.validate_event_time(event_data, event_data['start_time'], event_data['end_time'])
            activities_data = event_data.pop('activities', [])
            event = Event.objects.create(**event_data)
            for activity_data in activities_data:
                EventActivity.objects.create(
                    event=event,
                    activity_id=activity_data['activity_id'],
                    scheduled_time=activity_data['scheduled_time'],
                    created_by=user
                )
            return event
        
    def event_detail(self, event_id):
        try:
            event = (
            Event.objects
            .filter(id=event_id)
            .prefetch_related(
                # activities + vote count
                Prefetch(
                    "eventactivity_set",
                    queryset=EventActivity.objects.prefetch_related('votes__voted_by'),
                ),
                # participants
                Prefetch(
                    "eventattendant_set",
                    queryset=EventAttendant.objects.select_related("user"),
                ),
            )
            .first()
            )
            if not event:
                raise NotFound("Event not found")
            return event
        except Event.DoesNotExist:
            return None

    def validate_event_time(self, event, start_time, end_time):
        if start_time >= end_time:
            raise ValidationError("Start time must be before end time.")
        availability_exists = AvailabilityRule.objects.filter(
            rule_weekdays__weekday=(start_time).weekday(),
            start_time__lte=start_time.time(),
            end_time__gte=start_time.time(),
        )
        schedule_exists = Schedule.objects.filter(
            Q(start_time__lt=end_time, end_time__gt=start_time)
        )
        event_exists = Event.objects.filter(
            Q(start_time__lt=end_time, end_time__gt=start_time)
        )
        if event_exists.exists():
            raise ValidationError("The event time is overlap with another event.")
        if availability_exists.exists() or schedule_exists.exists():
            availability_discord_id = self.get_discord_ids(user_ids=availability_exists.values_list('user_id',flat=True))
            schedule_discord_id = self.get_discord_ids(user_ids=schedule_exists.values_list('created_by',flat=True))
            discord_id_conflict = availability_discord_id.union(schedule_discord_id)
            if discord_id_conflict is not None:
                DiscordNotificationService(bot_token=settings.DISCORD_BOT_TOKEN).notify_schedule_conflict(
                    channel_id=settings.DISCORD_CHANNEL_ID,
                    user_discord_id=discord_id_conflict,
                    event_title= event['title'],
                    ineligible_notification= event['ineligible_notification']
                )
        return True
    def get_discord_ids(self, user_ids):
        try:
            social_account = SocialAccount.objects.filter(user__id__in=user_ids, provider='discord').values_list('uid', flat=True)
            return social_account
        except SocialAccount.DoesNotExist:
            return None