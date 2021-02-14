from django.urls import path

from GinderApp.api.views import (
    ProfileAPIView,
    LikeUserPostAPIView,
    )

app_name = 'GinderApp'

urlpatterns = [
    path('profile/<int:pk>', ProfileAPIView.as_view(), name='profile'),
    path('like/<int:author_pk>', LikeUserPostAPIView.as_view(), name='like')
]
