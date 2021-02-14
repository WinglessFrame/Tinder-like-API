from django.contrib import admin
from GinderApp.models import Profile, Post, MatchChat, Message


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image', 'user')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'subscription')


class MatchChatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_profile1', 'user_profile2')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'chat', 'user')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(MatchChat, MatchChatAdmin)
admin.site.register(Message, MessageAdmin)
