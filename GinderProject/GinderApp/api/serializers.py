from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.reverse import reverse

from GinderApp.models import Profile, Post, MatchChat


# Profile serializers
class ProfileSerializer(ModelSerializer):
    lon = SerializerMethodField()
    lat = SerializerMethodField()
    subscription = SerializerMethodField()
    posts = SerializerMethodField()

    def get_lon(self, obj):
        if obj.location:
            return obj.location.x
        else:
            return "Not set"

    def get_lat(self, obj):
        if obj.location:
            return obj.location.y
        else:
            return "Not set"

    def get_subscription(self, obj):
        return obj.subscription

    def get_posts(self, obj):
        serializer = PostSerializer(obj.user.posts, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Profile
        fields = [
            'bio',
            'location',
            'lon',
            'lat',
            'subscription',
            'posts'
        ]


# Post serializers
class PostSerializer(ModelSerializer):
    user_profile_url = SerializerMethodField()
    like_url = SerializerMethodField()

    def get_user_profile_url(self, obj):
        request = self.context.get('request')
        return reverse('GinderApp:profile', args=[obj.user.profile.pk, ], request=request)

    def get_like_url(self, obj):
        request = self.context.get('request')
        return reverse('GinderApp:like', args=[obj.user.profile.pk], request=request)

    class Meta:
        model = Post
        fields = [
            'image',
            'description',
            'user_profile_url',
            'like_url',
        ]


# Chat Serializer
class ChatSerializer(ModelSerializer):
    user1 = SerializerMethodField()
    user2 = SerializerMethodField()

    def get_user1(self, obj):
        return obj.user_profile1.user.username

    def get_user2(self, obj):
        return obj.user_profile2.user.username

    class Meta:
        model = MatchChat
        fields = [
            'user1',
            'user2',
        ]
