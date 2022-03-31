from rest_framework import serializers
from .models import Client


class MembersSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='clients:member-detail')

    class Meta:
        model = Client
        fields = ('url', 'user', 'pk', 'get_longitude_latitude', 'last_name', 'first_name', 'photo', 'gender')
