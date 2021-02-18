from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .view import CustomTokenObtainPairView, RegisterAPIView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


