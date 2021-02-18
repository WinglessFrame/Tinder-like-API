from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField, PrimaryKeyRelatedField
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer
from rest_framework.reverse import reverse
from django.db.models import Q

from GinderApp.models import Profile, Post, MatchChat, Message


# Profile serializers
class ProfileSerializer(GeoModelSerializer):
    username = SerializerMethodField()
    subscription = SerializerMethodField()
    clear_viewed_url = SerializerMethodField()
    create_post_url = SerializerMethodField()
    posts = SerializerMethodField()
    matches = SerializerMethodField()
    search_distance = SerializerMethodField()
    change_search_distance_uri = SerializerMethodField()

    def get_change_search_distance_uri(self, obj):
        if obj.subscription != 'gold':
            return 'You have to buy Gold plan to change distance'
        return

    def get_search_distance(self, obj):
        return obj.search_distance

    def get_create_post_url(self, obj):
        return reverse('GinderApp:create_post', request=self.context.get('request'))

    def get_clear_viewed_url(self, obj):
        return reverse('GinderApp:clear', request=self.context.get('request'))

    def get_username(self, obj):
        return obj.user.username

    def get_subscription(self, obj):
        return obj.subscription

    def get_posts(self, obj):
        serializer = PostOwnerSerializer(obj.user.posts, many=True, context=self.context)
        return serializer.data

    def get_matches(self, obj):
        queryset = MatchChat.objects.filter(Q(user_profile1=obj) | Q(user_profile2=obj))
        matches_serializer = ListMatchChatSerializer(queryset, many=True, context=self.context)
        return matches_serializer.data

    class Meta:
        model = Profile
        geo_field = 'location'
        fields = [
            'username',
            'bio',
            'location',
            'subscription',
            'search_distance',
            'create_post_url',
            'clear_viewed_url',
            'matches',
            'posts'
        ]


# Post serializers
class PostSerializer(ModelSerializer):
    like_url = SerializerMethodField()

    def get_like_url(self, obj):
        request = self.context.get('request')
        return reverse('GinderApp:like', args=[obj.user.profile.pk], request=request)

    class Meta:
        model = Post
        fields = [
            'image',
            'description',
            'like_url',
        ]


# Post serializer for Owner (in profile)
class PostOwnerSerializer(ModelSerializer):
    delete_update_url = SerializerMethodField()

    def get_delete_update_url(self, obj):
        request = self.context.get('request')
        return reverse('GinderApp:update_delete_post', args=[obj.pk], request=request)

    class Meta:
        model = Post
        fields = [
            'image',
            'description',
            'delete_update_url'
        ]


class PostCreateSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        obj = Post.objects.create(user=self.context['request'].user,
                                  **validated_data)
        return obj

    class Meta:
        model = Post
        fields = (
            'image',
            'description',
            'user',
        )


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
