from rest_framework import serializers
from activities.models.activity import Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['title', 'id', 'description', 'price', 'created_by']
        read_only_fields = ['id']