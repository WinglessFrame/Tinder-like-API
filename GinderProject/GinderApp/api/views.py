from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.gis.measure import Distance

from GinderApp.api.permissions import (
    IsOwnerOrReadOnly,
    IsChatParticipant,
    IsLocationSet,
    IsPostOwner,
    IsGoldSubscription,
)
from GinderApp.api.serializers import (
    ProfileSerializer,
    ChatSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    ListMatchChatSerializer,
    PostSerializer,
    PostCreateSerializer,
    PostOwnerSerializer,
    UpdateSearchDistanceSerializer,
)
from GinderApp.api.api_utils import is_match, create_match
from GinderApp.models import Profile, MatchChat, Message, Post
from GinderApp.api.throttling import SubscriptionRateThrottle


# Profile views
class ProfileAPIView(RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related().get(pk=self.request.user.profile.pk)

    # overrides default one to skip lookup_field
    def get_object(self):
        queryset = self.get_queryset()
        return queryset


# Update search distance View. Only for gold subscription plan
class UpdateSearchDistanceAPIView(UpdateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsGoldSubscription]
    serializer_class = UpdateSearchDistanceSerializer

    def get_queryset(self):
        return Profile.objects.get(pk=self.request.user.profile.pk)

    # overrides default one to skip lookup_field
    def get_object(self):
        queryset = self.get_queryset()
        return queryset


# Like View
class LikeUserPostAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        post_author_pk = kwargs.get('author_pk')
        if not post_author_pk:
            return Response(data={"message": "Post author not found"}, status=404)
        post_author = Profile.objects.get(pk=post_author_pk)
        if user.profile == post_author:
            return Response(data={"message": "You cant like your own post"}, status=403)
        if is_match(user, post_author):
            chat_url = create_match(user.profile, post_author, request)
            return Response(data={
                "message": "Match!",
                "chat_url": chat_url
            }
                , status=201)
        else:
            return Response(data={"message": "Liked"}, status=201)


# Chat View
class ChatAPIView(RetrieveDestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsChatParticipant, ]
    serializer_class = ChatSerializer
    lookup_field = 'pk'
    queryset = MatchChat.objects.all()


# Send Message
class SendChatMessageAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageCreateSerializer

    def post(self, request, *args, **kwargs):
        chat_pk = kwargs.get("pk")
        text = request.data.get('text')
        image = request.data.get('image')
        chat = MatchChat.objects.get(pk=chat_pk)
        user_profile = request.user.profile
        if not (user_profile == chat.user_profile1 or user_profile == chat.user_profile2):
            return Response(data={'message': "You are not a chat participant"}, status=403)
        if chat:
            Message.objects.create(user=request.user.profile, text=text, image=image, chat=chat)
            return redirect('GinderApp:chat', pk=chat_pk)
        else:
            return Response(data={'message': 'chat not found'}, status=404)


# Swipes
class SwipesAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsLocationSet]
    throttle_classes = [SubscriptionRateThrottle]
    serializer_class = PostSerializer

    def get(self, request):
        request_user = request.user
        profile = request_user.profile
        distance = profile.search_distance
        post = Post.objects.select_related('user').filter(
            ~Q(user=request_user) &
            Q(user__profile__location__distance_lt=(
                profile.location, Distance(km=distance))) &  # TODO distance based on subscription
            ~Q(user__profile__in=profile.viewed.all())
        ).first()
        if not post:
            return Response(data=
                            {'message': 'found no one around',
                             'tip': f"You can try to clear viewed users in your profile"}
                            )
        profile.viewed.add(post.user.profile)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)


# Clear all viewed APIView
class ClearViewedAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        profile.viewed.clear()
        return Response(data={'message': 'Viewed users are available in swipes'}, status=201)


# Create post view
class CreatePostAPIView(CreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer


# update and delete post view
class UpdateDeletePostAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsPostOwner]
    serializer_class = PostOwnerSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        return user.posts.all()

