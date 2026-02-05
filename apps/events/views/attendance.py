from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from events.models.attendance import EventAttendant
from events.serializers.attendance_serializers import AttendanceSerializer
from events.services.attendance_service import AttendanceService
from rest_framework.response import Response
class AttendanceViewSet(ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EventAttendant.objects.filter(user=self.request.user)
    
    def create(self, request):
        serializer = AttendanceSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        AttendanceService().create(self.request.user, serializer.validated_data)
        return Response(serializer.data, status=201)