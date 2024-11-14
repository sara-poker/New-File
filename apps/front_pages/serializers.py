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

class IspSerializerr(serializers.ModelSerializer):
    name2 = serializers.SerializerMethodField()

    class Meta:
        model = Isp
        fields = '__all__'

    def get_name2(self, obj):
        return obj.name.replace(' ', '').lower()

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


class OnlineTestGetSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    name2 = serializers.SerializerMethodField()  # اضافه کردن فیلد name2

    class Meta:
        model = OnlineTest
        fields = '__all__'  # اضافه کردن name2 به لیست fields

    def get_date(self, obj):
        # تبدیل تاریخ به فرمت مورد نظر
        date_str = str(obj.date)
        return f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:]}"

    def get_name2(self, obj):
        # حذف فاصله‌ها از vpn_name
        return obj.vpn_name.replace(' ', '')

