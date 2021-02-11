from rest_framework.serializers import ModelSerializer, SerializerMethodField

from GinderApp.models import Profile, Post


# Profile serializers
class ProfileSerializer(ModelSerializer):
    lon = SerializerMethodField()
    lat = SerializerMethodField()

    def get_lon(self):
        if self.location:
            return self.location.LON
        else:
            return "Not set"

    def get_lat(self):
        if self.location:
            return self.location.LAT
        else:
            return "Not set"

    class Meta:
        model = Profile
        fields = [
            'bio',
            'lon',
            'lat'
            'subscription'
        ]