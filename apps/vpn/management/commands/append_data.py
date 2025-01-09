import pandas as pd
from django.core.management import BaseCommand
from django.db import transaction
from config.settings import BASE_DIR
from apps.vpn.models import Vpn, Country, Isp, Test
from apps.ticket.models import Notification  # مسیر صحیح مدل Notification
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Your help message for this command'

    def handle(self, *args, **options):
        # خواندن داده‌ها از فایل اکسل
        excel_data = pd.read_excel(BASE_DIR / 'data.xlsx')
        # جایگزینی NaN با None
        excel_data = excel_data.where(pd.notna(excel_data), None).values.tolist()
        count_data = len(excel_data)
        err_count = 0

        for counter, data in enumerate(excel_data, start=1):
            try:
                with transaction.atomic():
                    # تبدیل مقادیر به None برای فیلدهای مناسب
                    name = data[11] if data[11] is not None else None
                    platform = data[13] if data[13] is not None else None
                    vpn_maker = data[28] if data[28] is not None else None
                    country_name = data[29] if data[29] is not None else None
                    vpn_normal_user_fee = data[30] if data[30] is not None else None
                    isp_name = data[18] if data[18] is not None else None
                    server_country_name = data[19] if data[19] is not None else None
                    ping = -1 if data[25] == "failed" or pd.isna(data[25]) else int(data[25])
                    ttl = -1 if data[26] == "failed" or pd.isna(data[26]) else int(data[26])

                    # ایجاد یا دریافت VPN
                    vpn, vpn_created = Vpn.objects.get_or_create(
                        name=name.encode('utf-8', 'ignore').decode('utf-8') if name else None,
                        defaults={
                            "platform": platform,
                            "vpn_maker": vpn_maker,
                            "vpn_country": Country.objects.get_or_create(name=country_name)[0] if country_name else None,
                            "vpn_normal_user_fee": vpn_normal_user_fee
                        }
                    )

                    # ایجاد یا دریافت ISP
                    isp, isp_created = Isp.objects.get_or_create(name=isp_name) if isp_name else (None, False)

                    # ایجاد یا دریافت کشور سرور
                    server_country, country_created = Country.objects.get_or_create(
                        name=server_country_name) if server_country_name else (None, False)

                    # ایجاد Test
                    Test.objects.create(
                        date=int(data[0]) if not pd.isna(data[0]) else None,
                        time=data[7],
                        city=data[8].encode('utf-8', 'ignore').decode('utf-8') if data[8] else None,
                        vpn=vpn,
                        oprator=data[12] if data[12] else None,
                        status=data[14] if data[14] else None,
                        filter=data[15] if data[15] else None,
                        server_ip=data[16] if data[16] else None,
                        server_host=data[17] if data[17] else None,
                        server_isp=isp,
                        server_country=server_country,
                        server_region=data[20] if data[20] else None,
                        server_city=data[21] if data[21] else None,
                        server_Latitude=data[22] if data[22] else None,
                        server_Longitude=data[23] if data[23] else None,
                        ping_speed=ping,
                        ttl=ttl,
                        proxy_port=data[31] if len(data) > 31 and data[31] else None,
                        proxy_secret=data[32] if len(data) > 32 and data[32] else None,
                    )

                    # ارسال نوتیفیکیشن‌ها
                    users = User.objects.all()
                    user_is_staff = users.filter(is_staff=True)
                    if vpn_created:
                        for user in users:
                            Notification.objects.create(
                                user=user,
                                message=f"یک ابزار گریز جدید '{vpn.name}' ایجاد شد."
                            )

                    if isp_created:
                        for user in users:
                            Notification.objects.create(
                                user=user,
                                message=f"یک آی اس پی جدید '{isp.name}' ایجاد شد."
                            )

                    if country_created:
                        for user in user_is_staff:
                            Notification.objects.create(
                                user=user,
                                message=f"کشور جدید '{server_country.name}' ایجاد شد."
                            )

                print(f"{counter} from {count_data} Done! /{name}/")

            except Exception as e:
                print(f"Row {counter} Data: {data}")  # چاپ داده‌ای که خطا دارد
                self.stdout.write(self.style.ERROR(f"Error processing row {counter}: {e}"))
                err_count += 1
                continue

        print("the count of Error>>", err_count)
