from django.urls import path

from GinderApp.api.views import ProfileAPIView

app_name = 'GinderApp'

urlpatterns = [
    path('profile/<int:pk>', ProfileAPIView.as_view(), name='profile'),
]
