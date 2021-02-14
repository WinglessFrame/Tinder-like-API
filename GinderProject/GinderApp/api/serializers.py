from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.reverse import reverse

from GinderApp.models import Profile, Post, MatchChat, Message


# Profile serializers
class ProfileSerializer(ModelSerializer):
    username = SerializerMethodField()
    lon = SerializerMethodField()
    lat = SerializerMethodField()
    subscription = SerializerMethodField()
    posts = SerializerMethodField()
    matches = SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

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

    def get_matches(self, obj):
        request = self.context.get('request')
        if obj.user.profile == obj:
            return reverse('GinderApp:matches', request=request)
        else:
            return 'Forbidden'

    class Meta:
        model = Profile
        fields = [
            'username',
            'bio',
            'location',
            'lon',
            'lat',
            'subscription',
            'matches',
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


# Message Serializer
class MessageSerializer(ModelSerializer):
    user = SerializerMethodField()

    def get_user(self, obj):
        return obj.user.user.username

    class Meta:
        model = Message
        fields = [
            'user',
            'text',
            'image',
        ]


class MessageCreateSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'text',
            'image',
        ]


# Chat Serializer
class ChatSerializer(ModelSerializer):
    user1 = SerializerMethodField()
    user2 = SerializerMethodField()
    send_message_url = SerializerMethodField()
    messages = MessageSerializer(many=True)

    def get_user1(self, obj):
        return obj.user_profile1.user.username

    def get_user2(self, obj):
        return obj.user_profile2.user.username

    def get_send_message_url(self, obj):
        request = self.context.get('request')
        return reverse('GinderApp:message', args=[obj.pk], request=request)

    class Meta:
        model = MatchChat
        fields = [
            'user1',
            'user2',
            'send_message_url',
            'messages',
        ]


# List
class ListMatchChatSerializer(ModelSerializer):
    chat_url = SerializerMethodField()
    participants = SerializerMethodField()

    def get_chat_url(self, obj):
        request = self.context.get('request')
        return reverse('GinderApp:chat', args=[obj.pk], request=request)

    def get_participants(self, obj):
        return str(obj)

    class Meta:
        model = MatchChat
        fields = [
            'participants',
            'chat_url',
        ]
