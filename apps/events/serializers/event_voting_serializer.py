from rest_framework import serializers
from events.models.event_activities_voting import EventActivityVoting

class EventVotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventActivityVoting
        fields = ['id', 'event_activity', 'voted_by', 'voted_at', 'is_eligible']
        read_only_fields = ['id']