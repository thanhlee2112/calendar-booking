from rest_framework.routers import DefaultRouter
from events.views.event import EventViewSet
from events.views.attendance import AttendanceViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
urlpatterns = router.urls