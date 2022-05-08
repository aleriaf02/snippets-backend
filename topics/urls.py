from .views import TopicViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', TopicViewSet, basename='topic')

urlpatterns = router.urls
