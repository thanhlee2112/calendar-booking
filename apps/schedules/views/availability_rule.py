from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from schedules.services.availability_rule_services import AvailabilityRuleService
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, APIException
from rest_framework import status
from django.db.models import Q
from schedules.models.availability_rule import AvailabilityRule
from schedules.serializers.availability_rule_serializers import AvailabilityRuleSerializer

class AvailabilityRuleViewSet(ModelViewSet):
    serializer_class = AvailabilityRuleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Lấy params valid_from, valid_to từ request
        valid_from = self.request.query_params.get('valid_from')
        valid_to = self.request.query_params.get('valid_to')
        qs = AvailabilityRule.objects.filter(user=self.request.user).prefetch_related('rule_weekdays')
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
        serializer = AvailabilityRuleSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = AvailabilityRuleSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            instance = AvailabilityRuleService().create(self.request.user, serializer.validated_data)
            response_serializer = AvailabilityRuleSerializer(instance, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": '; '.join(e.messages)}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk=None):
        try:
            instance = self.get_object()
            AvailabilityRuleService().delete(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": '; '.join(e.messages)}, status=status.HTTP_400_BAD_REQUEST)