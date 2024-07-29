# serializers.py
from rest_framework import serializers
from apps.vpn.models import *


class VpnSerializerr(serializers.ModelSerializer):
    name2 = serializers.SerializerMethodField()

    class Meta:
        model = Vpn
        fields = '__all__'

    def get_name2(self, obj):
        return obj.name.replace(' ', '')


class VpnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vpn
        fields = ['id', 'name', 'platform', 'vpn_maker', 'vpn_country', 'vpn_normal_user_fee']


class IspSerializer(serializers.ModelSerializer):
    class Meta:
        model = Isp
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'date', 'time', 'city', 'vpn', 'oprator', 'status', 'filter', 'server_ip',
                  'server_host',
                  'server_isp', 'server_country', 'server_region', 'server_city', 'server_Latitude',
                  'server_Longitude', 'ping_speed', 'ttl', 'proxy_port', 'proxy_secret']

class OnlineTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineTest
        fields = '__all__'
