from rest_framework import permissions


class AnonPermissionsOnly(permissions.BasePermission):
    """
    Non-auth user only
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owner or read-only permission
    """
    message = "You must be an owner to update/delete this item"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class IsChatParticipant(permissions.BasePermission):
    message = "You must be participant of chat to enter conversation"

    def has_object_permission(self, request, view, obj):
        profile = request.user.profile
        return profile == obj.user_profile1 or profile == obj.user_profile2


class IsLocationSet(permissions.BasePermission):
    message = "You have to set location in profile"

    def has_permission(self, request, view):
        return request.user.profile.location


class IsPostOwner(permissions.BasePermission):
    message = "You is not a post owner"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsGoldSubscription(permissions.BasePermission):
    message = "you have to own gold subscription plan to update search distance"

    def has_permission(self, request, view):
        return request.user.profile.subscription == 'gold'
