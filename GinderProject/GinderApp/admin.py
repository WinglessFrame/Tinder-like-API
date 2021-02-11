from django.contrib import admin
from .models import Profile, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image', 'user')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'subscription')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
