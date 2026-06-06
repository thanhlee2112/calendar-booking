from rest_framework.routers import DefaultRouter
from apps.events.views.voting import EventActivityVotingViewSet
from events.views.event import EventViewSet
from events.views.attendance import AttendanceViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'voting', EventActivityVotingViewSet, basename='voting')
urlpatterns = router.urls