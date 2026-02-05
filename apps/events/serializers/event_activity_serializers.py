from rest_framework import serializers
from events.models.event_activities import EventActivity
from allauth.socialaccount.models import SocialAccount

class EventActivityDetailSerializers(serializers.ModelSerializer):
    activity_name = serializers.CharField(source='activity.name', read_only=True)
    voter = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = EventActivity
        fields = ['id', 'event', 'activity', 'scheduled_time', 'created_by']
        read_only_fields = ['id']

    def get_voter(self, obj):
        user_ids = [vote.voted_by.id for vote in obj.votes.all()]
        social_accounts = SocialAccount.objects.filter(user_id__in=user_ids, provider='discord')
        id_to_username = {sa.user_id: sa.extra_data.get('username', '') for sa in social_accounts}
        return [id_to_username[user_id] for user_id in user_ids]
