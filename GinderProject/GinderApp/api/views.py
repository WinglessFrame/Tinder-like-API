from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from GinderApp.api.permissions import IsOwnerOrReadOnly
from GinderApp.api.serializers import ProfileSerializer
from GinderApp.models import Profile


# Profile views
class ProfileAPIView(RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly,]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
