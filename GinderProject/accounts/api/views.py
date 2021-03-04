from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.permissions import AnonPermissionsOnly
from accounts.api.serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class RegisterAPIView(generics.CreateAPIView):
    queryset = User
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionsOnly, ]

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}
