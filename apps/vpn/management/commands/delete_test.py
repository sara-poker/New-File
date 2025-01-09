from django.core.management import BaseCommand
from apps.vpn.models import Test

class Command(BaseCommand):
    help = 'Delete the specified number of rows from the end of the Test table'

    def add_arguments(self, parser):
        # Adding an argument to accept the number of rows to delete
        parser.add_argument('count', type=int, help='Number of rows to delete from the end of the table')

    def handle(self, *args, **options):
        count = options['count']  # Getting the input number

        # Extract IDs of the last 'count' rows
        row_ids = list(
            Test.objects.order_by('-id')
            .values_list('id', flat=True)[:count]
        )

        if row_ids:
            # Delete rows using the extracted IDs
            deleted_count, _ = Test.objects.filter(id__in=row_ids).delete()
            self.stdout.write(f"Successfully deleted {deleted_count} rows from the Test table.")
        else:
            self.stdout.write("No rows to delete in the Test table.")
