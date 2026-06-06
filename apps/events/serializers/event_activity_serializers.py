from rest_framework import serializers
from events.models.event_activities import EventActivity
from allauth.socialaccount.models import SocialAccount

class EventActivityDetailSerializers(serializers.ModelSerializer):
    activity_title = serializers.CharField(source='activity.title', read_only=True)
    activity_description = serializers.CharField(source='activity.description', read_only=True)
    activity_price = serializers.CharField(source='activity.price', read_only=True)
    activity_link = serializers.CharField(source='activity.link', read_only=True)
    voter = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = EventActivity
        fields = ['id', 'event', 'activity', 'created_by', 'voter', 'activity_title', 'activity_description', 'activity_price', 'activity_link']
        read_only_fields = ['id']
        unique_together = ['event', 'activity']

    def get_voter(self, obj):
        eligible_votes = obj.votes.filter(is_eligible=True)
        user_ids = [vote.voted_by.id for vote in eligible_votes]
        social_accounts = SocialAccount.objects.filter(user_id__in=user_ids, provider='discord')
        id_to_username = {sa.user_id: sa.extra_data.get('username', '') for sa in social_accounts}
        return [{'username': id_to_username[user_id], 'user_id': user_id} for user_id in user_ids]
