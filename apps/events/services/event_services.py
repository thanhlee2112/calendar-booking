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
            discord_id_conflict = self.validate_event_time(event_data, event_data['start_time'], event_data['end_time'])
            if discord_id_conflict is not None:
                social_account = SocialAccount.objects.filter(uid__notin=discord_id_conflict, provider='discord').values_list('uid', flat=True)
            else:
                social_account = SocialAccount.objects.filter(provider='discord').values_list('uid', flat=True)
            activities_data = event_data.pop('activities', [])
            event = Event.objects.create(**event_data)
            for activity_data in activities_data:
                EventActivity.objects.create(
                    event=event,
                    activity_id=activity_data,
                    created_by=user
                )
            DiscordNotificationService(bot_token=settings.DISCORD_BOT_TOKEN).send_notification(
                channel_id=settings.DISCORD_CHANNEL_ID,
                user_discord_id=social_account,
                notification_message= event_data['eligible_notification']
            )
            return event
        
    def event_detail(self, event_id):
        try:
            print(event_id)
            event = (
            Event.objects
            .filter(id=event_id)
            .prefetch_related(
                # activities + vote count
                Prefetch(
                    "eventactivity_set",
                    queryset=EventActivity.objects.select_related('activity').prefetch_related('votes__voted_by'),
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
                DiscordNotificationService(bot_token=settings.DISCORD_BOT_TOKEN).send_notification(
                    channel_id=settings.DISCORD_CHANNEL_ID,
                    user_discord_id=discord_id_conflict,
                    event_title= event['title'],
                    ineligible_notification= event['ineligible_notification']
                )
                return discord_id_conflict
        return True
    def get_discord_ids(self, user_ids):
        try:
            social_account = SocialAccount.objects.filter(user__id__in=user_ids, provider='discord').values_list('uid', flat=True)
            return social_account
        except SocialAccount.DoesNotExist:
            return None
        
    def update_event(self, event_id, event_data, user):
        try:
            event = Event.objects.get(id=event_id)
            if event.created_by != user:
                raise ValidationError("You do not have permission to update this event.")
            activities_data = event_data.pop('activities', None)
            # Kiểm tra unique_together cho start_time, end_time, loại trừ event hiện tại
            new_start_time = event_data.get('start_time', event.start_time)
            new_end_time = event_data.get('end_time', event.end_time)
            if Event.objects.filter(start_time=new_start_time, end_time=new_end_time).exclude(id=event_id).exists():
                raise ValidationError("The fields start_time, end_time must make a unique set.")
            for key, value in event_data.items():
                setattr(event, key, value)
            event.save()
            for activity_data in activities_data:
                EventActivity.objects.update_or_create(
                    event=event,
                    activity_id=activity_data,
                    defaults={'created_by': user}
                )
            return event
        except Event.DoesNotExist:
            raise NotFound("Event not found.")