from rest_framework.routers import DefaultRouter
from schedules.views.availability_rule import AvailabilityRuleViewSet

router = DefaultRouter()
router.register(r'availability-rules', AvailabilityRuleViewSet, basename='availability-rule')
urlpatterns = router.urls