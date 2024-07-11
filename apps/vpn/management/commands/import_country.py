from django.core.management import BaseCommand
import json

from config.settings import BASE_DIR
from apps.vpn.models import Country



class Command(BaseCommand):
    help = 'Your help message for this command'

    def handle(self, *args, **options):
        json_file_path = BASE_DIR / 'country.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for country_data in data:
            country, created = Country.objects.get_or_create(
                name=country_data['title'],
                defaults={
                    'country_id': country_data['id'],
                    'continent': country_data['continent'],
                    'population': country_data['value'],
                    'flag': country_data.get('flag', None),
                    'persian_name': country_data.get('title_fa', None)
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added country {country.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Country {country.name} already exists'))
