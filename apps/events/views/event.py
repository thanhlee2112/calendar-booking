from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from events.models.event import Event
from events.serializers.event_serializers import EventSerializer
from events.services.event_services import EventService
from events.serializers.event_detail_serializers import EventDetailSerializer
from rest_framework.response import Response
class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)
    
    def create(self, request):
        serializer = EventSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        EventService().create_event(
            user=self.request.user,
            event_data=serializer.validated_data,
        )
        return Response("here", status=201)
        
    def retrieve(self, request, pk=None):
        event = EventService().event_detail(pk)
        serializer = EventDetailSerializer(event, context={'request': request})
        return Response(serializer.data)