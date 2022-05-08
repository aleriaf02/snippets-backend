from .views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = router.urls