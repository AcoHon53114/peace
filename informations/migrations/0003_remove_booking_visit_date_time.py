# Generated by Django 5.1.1 on 2024-10-01 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('informations', '0002_booking_visit_date_booking_visit_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='visit_date_time',
        ),
    ]
