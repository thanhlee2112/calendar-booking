from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from activities.models.activity import Activity
from activities.serializers.activities_serializers import ActivitySerializer

class ActivityViewSet(ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()