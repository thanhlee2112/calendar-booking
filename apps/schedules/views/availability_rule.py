from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from schedules.services.availability_rule_services import AvailabilityRuleService

from schedules.models.availability_rule import AvailabilityRule
from schedules.serializers.availability_rule_serializers import AvailabilityRuleSerializer

class AvailabilityRuleViewSet(ModelViewSet):
    serializer_class = AvailabilityRuleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Limit to availability rules of the authenticated user
        return AvailabilityRule.objects.filter(user=self.request.user).prefetch_related('rule_weekdays')
    
    def perform_create(self, serializer):
        # Set the user to the authenticated user on creation
        serializer.is_valid()
        AvailabilityRuleService().create(self.request.user, serializer.validated_data)