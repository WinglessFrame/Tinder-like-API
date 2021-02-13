from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # Main-app
    path('app/api/', include('GinderApp.api.urls', namespace='GinderApp')),
    # JWT login / register / refresh
    path('api/accounts/', include('accounts.api.urls', namespace='accounts')),
    # DRF login / register
    path('api-auth/', include('rest_framework.urls', namespace='auth')),

]
