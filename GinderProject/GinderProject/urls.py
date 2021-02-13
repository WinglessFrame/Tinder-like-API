from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # Main-app
    path('app/api/', include('GinderApp.api.urls', namespace='GinderApp')),
    # JWT login / register / refresh
    path('api/accounts/', include('accounts.api.urls', namespace='accounts')),
    # DRF login / register
    path('api-auth/', include('rest_framework.urls', namespace='auth')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
