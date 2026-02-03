from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from schedules.services.schedule_services import ScheduleService
from rest_framework.response import Response

from django.core.exceptions import ValidationError

from schedules.models.schedules import Schedule
from schedules.serializers.schedule_serializers import ScheduleSerializer

class ScheduleViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        # Limit to schedules of the authenticated user
        return Schedule.objects.filter(created_by=self.request.user)
    def create(self, request):
        # Set the user to the authenticated user on creation
        serializer = ScheduleSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            ScheduleService().create(self.request.user, serializer.validated_data)
            return Response(serializer.data, status=201)
        except ValidationError as e:
            return Response({'detail': e.message}, status=400)