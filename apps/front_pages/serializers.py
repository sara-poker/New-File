# serializers.py
from rest_framework import serializers
from apps.vpn.models import *

class VpnSerializer(serializers.ModelSerializer):
    name2 = serializers.SerializerMethodField()

    class Meta:
        model = Vpn
        fields = '__all__'

    def get_name2(self, obj):
        return obj.name.replace(' ', '')
