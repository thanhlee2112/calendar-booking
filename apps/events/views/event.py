from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from events.models.event import Event
from events.serializers.event_serializers import EventSerializer


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
