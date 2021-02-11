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


class AuthView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "You are already authenticated"}, status=400)
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if not username or not password:
            return Response({'detail': "Password or username are empty"})
        user = authenticate(username=username, password=password)
        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        )
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                response = get_tokens_for_user(user)
                return Response(response)
        return Response({'detail': 'Invalid credentials'}, status=401)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionsOnly,]

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}

# noinspection PyUnreachableCode
# class RegisterAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({"detail": "You are already authenticated"}, status=400)
#         data = request.data
#         username = data.get('username', None)
#         email = data.get('email', None)
#         password = data.get('password', None)
#         password2 = data.get('password2', None)
#         if password != password2:
#             return Response({"password": "Password must match"}, status=401)
#         qs = User.objects.filter(
#             Q(username__iexact=username) |
#             Q(email__iexact=username)
#         )
#         if qs.exists():
#             return Response({"detail" : "This user is already exist"}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             return Response({"detail": "Thanks for registering"},status=200)
