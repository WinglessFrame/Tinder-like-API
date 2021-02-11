from rest_framework.serializers import ModelSerializer, SerializerMethodField

from GinderApp.models import Profile, Post


# Profile serializers
class ProfileSerializer(ModelSerializer):
    lon = SerializerMethodField()
    lat = SerializerMethodField()

    def get_lon(self, obj):
        if obj.location:
            return obj.location.LON
        else:
            return "Not set"

    def get_lat(self, obj):
        if obj.location:
            return obj.location.LAT
        else:
            return "Not set"

    class Meta:
        model = Profile
        fields = [
            'bio',
            'lon',
            'lat',
        ]