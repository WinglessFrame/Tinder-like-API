from django.urls import path, re_path

from GinderApp.api.views import (
    ProfileAPIView,
    LikeUserPostAPIView,
    ChatAPIView,
    SendChatMessageAPIView,
    MatchesListAPIView,
    )

app_name = 'GinderApp'

urlpatterns = [
    path('profile/<int:pk>', ProfileAPIView.as_view(), name='profile'),
    path('like/<int:author_pk>', LikeUserPostAPIView.as_view(), name='like'),
    path('matches/', MatchesListAPIView.as_view(), name='matches'),
    path('chat/<int:pk>', ChatAPIView.as_view(), name='chat'),
    path('chat/<int:pk>/message', SendChatMessageAPIView.as_view(), name='message')
]
