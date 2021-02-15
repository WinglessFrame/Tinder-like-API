from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import redirect
from django.db.models import Q

from GinderApp.api.permissions import IsOwnerOrReadOnly, IsChatParticipant
from GinderApp.api.serializers import (
    ProfileSerializer,
    ChatSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    ListMatchChatSerializer,
    )
from GinderApp.api.api_utils import is_match, create_match
from GinderApp.models import Profile, MatchChat, Message
from GinderApp.api.throttling import SubscriptionRateThrottle


# Profile views
class ProfileAPIView(RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly, ]
    # throttle_classes = [SubscriptionRateThrottle,]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


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
class ChatAPIView(RetrieveAPIView):
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
        if user_profile == chat.user_profile1 or user_profile == chat.user_profile2:
            return Response(data={'message': "You are not a chat participant"}, status=403)
        if chat:
            Message.objects.create(user=request.user.profile, text=text, image=image, chat=chat)
            return redirect('GinderApp:chat', pk=chat_pk)
        else: return Response(data={'message': 'chat not found'}, status=404)


# Matches views
class MatchesListAPIView(ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ListMatchChatSerializer

    def get_queryset(self):
        user_profile = self.request.user.profile
        queryset = MatchChat.objects.filter(Q(user_profile1 = user_profile) | Q(user_profile2 = user_profile))
        return queryset
