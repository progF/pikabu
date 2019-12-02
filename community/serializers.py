from rest_framework import serializers
from community.models import Community, CommunityMember
from users.serializers import MainUserSerializer
from community.models import Community


class CommunityShortSerializer(serializers.ModelSerializer):
    creator = MainUserSerializer(read_only=True)

    class Meta:
        model = Community
        fields = ('id', 'name', 'creator', 'community_image')



class CommunitySerializer(CommunityShortSerializer):

    class Meta:
        model = Community
        fields = '__all__'
    