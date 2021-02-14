from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from GinderApp.api.permissions import IsOwnerOrReadOnly
from GinderApp.api.serializers import ProfileSerializer
from GinderApp.api.api_utils import is_match
from GinderApp.models import Profile
from GinderApp.api.throttling import SubscriptionRateThrottle


# Profile views
class ProfileAPIView(RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly,]
    # throttle_classes = [SubscriptionRateThrottle,]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


# Like View
class LikeUserPostAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        user = request.user
        post_author_pk = kwargs.get('author_pk')
        if not post_author_pk:
            return Response(data={"message": "Post author not found"}, status=404)
        post_author = Profile.objects.get(pk=post_author_pk)
        if user.profile == post_author:
            return Response(data={"message": "You cant like your own post"}, status=403)
        if is_match(user, post_author):
            create_match(user.profile, post_author)
            return Response(data={"message": "Match!"}, status=201)
        else:
            return Response(data={"message": "Liked"}, status=201)