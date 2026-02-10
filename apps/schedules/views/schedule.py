from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from schedules.services.schedule_services import ScheduleService
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from django.core.exceptions import ValidationError

from schedules.models.schedules import Schedule
from schedules.serializers.schedule_serializers import ScheduleSerializer

class ScheduleViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        # Limit to schedules of the authenticated user
        valid_from = self.request.query_params.get('valid_from')
        valid_to = self.request.query_params.get('valid_to')
        qs = Schedule.objects.filter(created_by=self.request.user)
        if valid_from or valid_to:
            null_filter = Q(valid_from__isnull=True) | Q(valid_to__isnull=True)
            range_filter = Q()
            if valid_from:
                range_filter &= Q(valid_from__gte=valid_from)
            if valid_to:
                range_filter &= Q(valid_to__lte=valid_to)
            qs = qs.filter(null_filter | range_filter)
        return qs
    
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        queryset = self.get_queryset()
        serializer = ScheduleSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        # Set the user to the authenticated user on creation
        serializer = ScheduleSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            ScheduleService().create(self.request.user, serializer.validated_data)
            return Response(serializer.data, status=201)
        except ValidationError as e:
            return Response({'detail': e.message}, status=400)
        
    def delete(self, request, pk=None):
        try:
            instance = self.get_object()
            ScheduleService().delete(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": '; '.join(e.messages)}, status=status.HTTP_400_BAD_REQUEST)