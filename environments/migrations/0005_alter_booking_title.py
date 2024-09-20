# Generated by Django 5.1.1 on 2024-09-20 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environments', '0004_booking_visit_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='title',
            field=models.CharField(choices=[('visiting', '預約參觀選位')], default='預約參觀選位', max_length=20),
        ),
    ]
