from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Update collation of database tables to utf8mb4_general_ci'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # تغییر collation پیش‌فرض پایگاه داده
            cursor.execute("ALTER DATABASE `%s` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;" % connection.settings_dict['NAME'])

            # دریافت لیست تمام جداول
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()

            # تغییر collation تمام جداول و ستون‌ها
            for table in tables:
                table_name = table[0]
                self.stdout.write("Updating table: %s" % table_name)
                cursor.execute("ALTER TABLE `%s` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;" % table_name)

        self.stdout.write(self.style.SUCCESS("Successfully updated collation of all tables to utf8mb4_general_ci"))
