from django.urls import path, re_path

from GinderApp.api.views import (
    ProfileAPIView,
    LikeUserPostAPIView,
    ChatAPIView,
    SendChatMessageAPIView,
    SwipesAPIView,
    ClearViewedAPIView,
    CreatePostAPIView,
    UpdateDeletePostAPIView,
    UpdateSearchDistanceAPIView,
    )

app_name = 'GinderApp'

urlpatterns = [
    # main app endpoint
    path('swipes', SwipesAPIView.as_view(), name='swipes'),
    path('swipes/like/<int:author_pk>', LikeUserPostAPIView.as_view(), name='like'),
    # profile settings and info
    path('profile', ProfileAPIView.as_view(), name='profile'),
    path('profile/change_distance', UpdateSearchDistanceAPIView.as_view(), name='update_distance'),
    path('profile/clear', ClearViewedAPIView.as_view(), name='clear'),
    path('profile/add_post', CreatePostAPIView.as_view(), name='create_post'),
    path('profile/posts/<int:pk>', UpdateDeletePostAPIView.as_view(), name='update_delete_post'),
    # endpoints
    path('chat/<int:pk>', ChatAPIView.as_view(), name='chat'),
    path('chat/<int:pk>/message', SendChatMessageAPIView.as_view(), name='message')
]
