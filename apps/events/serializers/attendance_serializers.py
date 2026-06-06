from rest_framework import serializers
from events.models.attendance import EventAttendant
from allauth.socialaccount.models import SocialAccount

class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    username = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = EventAttendant
        fields = ['event', 'user', 'attended_at', 'username','user_id']

    def get_username(self, obj):
        # Nếu obj là instance model
        if hasattr(obj, 'user') and obj.user:
            return obj.user.username
        # Nếu obj là dict (trường hợp hiếm, chỉ khi serialize dict)
        if isinstance(obj, dict) and 'user' in obj:
            return obj['user']
        return None
