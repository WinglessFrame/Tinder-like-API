from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
      # admin
      path('admin/', admin.site.urls),
      # Main-app
      path('app/api/', include('GinderApp.api.urls', namespace='GinderApp')),
      # JWT login / register / refresh
      path('jwt/', include('accounts.api.urls', namespace='accounts')),
      # DRF login / register
      path('api-auth/', include('rest_framework.urls', namespace='auth')),
      # debug Toolbar
      path('__debug__/', include(debug_toolbar.urls)),
      # Schema
      path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
      path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
      path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

