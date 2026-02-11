from rest_framework import serializers
from activities.models.activity import Activity

class ActivitySerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Activity
        fields = ['title', 'id', 'description', 'price', 'created_by', 'link']
        read_only_fields = ['id']