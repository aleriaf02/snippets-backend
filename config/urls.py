from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('admin/', admin.site.urls),
   # path('dj-rest-auth/', include('dj_rest_auth.urls')),
   path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
   path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   path('api/auth/', include('authentication.urls')),
   path('api/users/', include('users.urls')),
   path('api/snippets/', include('snippets.urls')),
   path('api/topics/', include('topics.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
