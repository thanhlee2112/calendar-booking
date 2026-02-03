from rest_framework.routers import DefaultRouter
from activities.views.activities import ActivityViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='')

urlpatterns = router.urls