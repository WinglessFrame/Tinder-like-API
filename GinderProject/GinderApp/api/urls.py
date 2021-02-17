from django.urls import path, re_path

from GinderApp.api.views import (
    ProfileAPIView,
    LikeUserPostAPIView,
    ChatAPIView,
    SendChatMessageAPIView,
    MatchesListAPIView,
    SwipesAPIView,
    ClearViewedAPIView,
    )

app_name = 'GinderApp'

urlpatterns = [
    # main app endpoint
    path('swipes', SwipesAPIView.as_view(), name='swipes'),
    path('swipes/like/<int:author_pk>', LikeUserPostAPIView.as_view(), name='like'),
    # profile manipulations
    path('profile', ProfileAPIView.as_view(), name='profile'),
    path('profile/clear', ClearViewedAPIView.as_view(), name='clear'),
    path('profile/matches', MatchesListAPIView.as_view(), name='matches'),
    # endpoints
    path('chat/<int:pk>', ChatAPIView.as_view(), name='chat'),
    path('chat/<int:pk>/message', SendChatMessageAPIView.as_view(), name='message')
]
