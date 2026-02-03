from rest_framework.routers import DefaultRouter
from schedules.views.availability_rule import AvailabilityRuleViewSet
from schedules.views.schedule import ScheduleViewSet

router = DefaultRouter()
router.register(r'availability-rules', AvailabilityRuleViewSet, basename='availability-rule')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
urlpatterns = router.urls