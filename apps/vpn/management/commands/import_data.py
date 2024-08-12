import pandas as pd
from django.core.management import BaseCommand
import math

from config.settings import BASE_DIR
from apps.vpn.models import *
from apps.ticket.models import Notification
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Your help message for this command'

    def handle(self, *args, **options):
        excel_data = pd.read_excel(BASE_DIR / 'data.xlsx')
        excel_data = excel_data.values.tolist()
        users = User.objects.all()
        count_data = len(excel_data)
        counter = 0

        for data in excel_data:
            counter += 1
            vpn_exist = Vpn.objects.filter(name=data[11])
            if vpn_exist:
                vpn_id = vpn_exist[0].id

            else:
                vpn_country_obj = Country.objects.filter(name=data[29]).first()
                if not vpn_country_obj:
                    vpn_country_obj = Country.objects.create(name=data[29])

                    for user in users:
                        notification = Notification.objects.create(
                            user=user,
                            message=f"کشور {vpn_country_obj.name} به دیتابیس اضافه شده است."
                        )

                vpn_data = {
                    "name": data[11],
                    "platform": data[13],
                    "vpn_maker": data[28],
                    "vpn_country": vpn_country_obj,
                    "vpn_normal_user_fee": data[30]
                }
                vpn = Vpn.objects.create(**vpn_data)
                vpn_id = vpn.id

            vpn = Vpn.objects.get(id=vpn_id)

            isp_exist = Isp.objects.filter(name=data[18])

            if isp_exist:
                isp_id = isp_exist[0].id
            else:
                isp_data = {
                    "name": data[18]
                }
                isp = Isp.objects.create(**isp_data)
                isp_id = isp.id

            isp = Isp.objects.get(id=isp_id)

            if data[25] == "failed" or math.isnan(data[25]):
                ping = -1
            else:
                ping = int(data[25])

            if data[26] == "failed" or math.isnan(data[26]):
                ttl = -1
            else:
                ttl = int(data[26])

            server_country_obj = Country.objects.filter(name=data[19]).first()
            if not server_country_obj:
                server_country_obj = Country.objects.create(name=data[19])
                server_country_obj = None

            test_data = {
                "date": int(data[0]),
                "time": data[7],
                "city": data[8],
                "vpn": vpn,
                "oprator": data[12],
                "status": data[14],
                "filter": data[15],
                "server_ip": data[16],
                "server_host": data[17],
                "server_isp": data[18],
                "server_country": server_country_obj,
                "server_region": data[20],
                "server_city": data[21],
                "server_Latitude": data[22],
                "server_Longitude": data[23],
                "ping_speed": ping,
                "ttl": ttl,
                "proxy_port": data[31],
                "proxy_secret": data[32],
            }

            test = Test.objects.create(**test_data)
            print(f"{counter} from {count_data} Done!")
