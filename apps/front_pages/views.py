from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.vpn.models import *
from apps.front_pages.serializers import *
from rest_framework import status
import math

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to front_pages/urls.py file for more pages.
"""


def filter_country(country, queryset):
    if country == "0":
        return queryset
    return queryset.filter(vpn_country=country)


def filter_country_server(country_server, queryset):
    if country_server == "0":
        return queryset
    return queryset.filter(vpns__server_country_id=country_server).distinct()


class FrontPagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,  # Get the current url path (active URL) from request
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        return context


class LandingView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class GetAllVpn(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        vpn = Vpn.objects.exclude(platform="Telegram")
        selected_country = self.request.GET.get('country')
        selected_country_server = self.request.GET.get('server_country')

        if selected_country:
            vpn = filter_country(selected_country, vpn)

        if selected_country_server:
            vpn = filter_country_server(selected_country_server, vpn)

        for item in vpn:
            original_name = item.name
            modified_name = original_name.replace(' ', '')
            item.name2 = modified_name

        serializer = VpnSerializerr(vpn, many=True)
        return Response(serializer.data)


class AddItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # Vpn
        vpn_exist = Vpn.objects.filter(name=data['vpn_name'])
        if vpn_exist:
            vpn = vpn_exist[0]
        else:
            vpn_country_obj = Country.objects.filter(name=data['vpn_country']).first()
            if not vpn_country_obj:
                vpn_country_obj = Country.objects.create(name=data['vpn_country'])

            vpn_data = {
                "name": data['vpn_name'],
                "platform": data['vpn_platform'],
                "vpn_maker": data['vpn_maker'],
                "vpn_country": vpn_country_obj.id,
                "vpn_normal_user_fee": data['vpn_normal_user_fee']
            }
            vpn_serializer = VpnSerializer(data=vpn_data)
            if vpn_serializer.is_valid():
                vpn = vpn_serializer.save()
            else:
                return Response(vpn_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Isp
        isp_exist = Isp.objects.filter(name=data['server_isp'])
        if isp_exist:
            isp = isp_exist[0]
        else:
            isp_data = {
                "name": data['server_isp']
            }
            isp_serializer = IspSerializer(data=isp_data)
            if isp_serializer.is_valid():
                isp = isp_serializer.save()
            else:
                return Response(isp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Ping and TTL
        if data['ping_speed'] == "failed" or math.isnan(data['ping_speed']):
            ping = -1
        else:
            ping = int(data['ping_speed'])

        if data['ttl'] == "failed" or math.isnan(data['ttl']):
            ttl = -1
        else:
            ttl = int(data['ttl'])

        # Server Country
        server_country_obj = Country.objects.filter(name=data['server_country']).first()
        if not server_country_obj:
            server_country_obj = Country.objects.create(name=data['server_country'])

        test_data = {
            "date": data['date'],
            "time": data['time'],
            "city": data['city'],
            "vpn": vpn.id,
            "oprator": data['oprator'],
            "status": data['status'],
            "filter": data['filter'],
            "server_ip": data['server_ip'],
            "server_host": data['server_host'],
            "server_isp": isp.id,
            "server_country": server_country_obj.id,
            "server_region": data['server_region'],
            "server_city": data['server_city'],
            "server_Latitude": data['server_Latitude'],
            "server_Longitude": data['server_Longitude'],
            "ping_speed": ping,
            "ttl": ttl,
            "proxy_port": data['proxy_port'],
            "proxy_secret": data['proxy_secret'],
        }

        test_serializer = TestSerializer(data=test_data)
        if test_serializer.is_valid():
            test_serializer.save()
            return Response(test_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddRecord(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        test_data = {
            "vpn_name": data['vpn_name'],
            "date": data['date'],
            "time": data['time'],
            "city": data['city'],
            "oprator": data['oprator'],
            "status": data['status']
        }

        online_test_serializer = OnlineTestSerializer(data=test_data)
        if online_test_serializer.is_valid():
            online_test_serializer.save()
            return Response(online_test_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(online_test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllRecord(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        online_test = OnlineTest.objects.all().order_by('-id')[:50]
        online_test = online_test[::-1]
        online_test_serializer = OnlineTestGetSerializer(online_test, many=True)

        return Response(online_test_serializer.data, status=status.HTTP_200_OK)
