from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Workspace, WorkspaceMember
from .serializers import WorkspaceSerializer
# Create your views here.

class WorkspaceListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workspaces = Workspace.objects.filter(owner=request.user)
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            WorkspaceMember.objects.create(
                workspace_id=serializer.data['id'],
                user=request.user
                role='owner'
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
