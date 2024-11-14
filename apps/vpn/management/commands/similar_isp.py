import json
from django.core.management.base import BaseCommand
from apps.vpn.models import Isp, Country

from config.settings import BASE_DIR

class Command(BaseCommand):
    help = 'Update Isp data from JSON'

    def handle(self, *args, **kwargs):
        # آدرس فایل JSON را در اینجا مشخص کنید
        json_file_path = BASE_DIR / 'isp.json'

        try:
            # خواندن داده‌ها از فایل JSON
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {json_file_path}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error decoding JSON'))
            return

        for item in data:
            try:
                # به‌روزرسانی URL
                isp = Isp.objects.get(id=item['id'])
                isp.url = item['url']

                # پیدا کردن کشور با توجه به نام
                country = Country.objects.get(name=item['country_id'])
                isp.country = country

                isp.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated ISP: {isp.name}'))
            except Country.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Country does not exist: {item["country_id"]}'))
            except Isp.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'ISP does not exist with id: {item["id"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error updating ISP {item["id"]}: {str(e)}'))
