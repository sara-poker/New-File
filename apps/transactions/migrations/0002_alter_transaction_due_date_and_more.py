# Generated by Django 5.0 on 2024-04-24 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='due_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateField(),
        ),
    ]
