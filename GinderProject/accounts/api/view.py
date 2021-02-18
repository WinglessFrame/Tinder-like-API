from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import AnonPermissionsOnly
from .serializer import CustomTokenObtainPairSerializer, UserRegisterSerializer
from .utils import get_tokens_for_user

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
