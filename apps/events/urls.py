from rest_framework.routers import DefaultRouter
from events.views.event import EventViewSet

router = DefaultRouter()
router.register(r'', EventViewSet, basename='')
urlpatterns = router.urls