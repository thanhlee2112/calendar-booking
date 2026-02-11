from rest_framework import viewsets, permissions
from rest_framework.response import Response
from events.models.event_activities_voting import EventActivityVoting
from events.serializers.event_voting_serializer import EventVotingSerializer
from events.services.voting_services import VotingService
class EventActivityVotingViewSet(viewsets.ModelViewSet):
    queryset = EventActivityVoting.objects.all()
    serializer_class = EventVotingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        voting_service = VotingService()
        response = voting_service.vote(request.user, request.data)
        return Response({"message": response}, status=204)
    
    def destroy(self,request, pk=None):
        voting_service = VotingService()
        response = voting_service.remove_vote(request.user, pk)
        return Response({"message": response}, status=204)