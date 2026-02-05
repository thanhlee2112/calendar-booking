from rest_framework import serializers
from events.models.attendance import EventAttendant
from allauth.socialaccount.models import SocialAccount

class AttendanceSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = EventAttendant
        fields = ['event', 'user', 'attended_at','username']

    def get_username(self, obj):
        social_account = SocialAccount.objects.filter(user=obj.user).first()
        return social_account.extra_data.get('username', '')