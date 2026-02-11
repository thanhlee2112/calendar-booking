from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from events.models.attendance import EventAttendant
from events.models.event_activities_voting import EventActivityVoting
from events.serializers.attendance_serializers import AttendanceSerializer
from events.services.attendance_service import AttendanceService
from events.services.voting_services import VotingService
from rest_framework.response import Response
class AttendanceViewSet(ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EventAttendant.objects.filter(user=self.request.user)
    
    def create(self, request):
        AttendanceService().create(self.request.user, request.data)
        return Response({"message": "Attendance created successfully."}, status=201)

    @action(detail=False, methods=['post'], url_path='attend-and-vote')
    def attendAndVote(self, request):
        attendance = AttendanceService().create(self.request.user, request.data)
        # Gọi service để vote cho hoạt động được đề xuất tốt nhất của sự kiện
        VotingService().vote(self.request.user, request.data)
        return Response('Attendance and vote successfully', status=201)
    
    def destroy(self, request, pk=None):
        attendance = EventAttendant.objects.filter(event=pk, user=self.request.user).first()
        voting = EventActivityVoting.objects.filter(event_activity__event_id=pk, voted_by=self.request.user).first()
        if not attendance:
            return Response({"error": "Attendance not found."}, status=404)
        attendance.delete()
        if voting:
            voting.delete()
        return Response({"message": "Attendance deleted successfully."}, status=204)