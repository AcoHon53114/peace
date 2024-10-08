# Generated by Django 5.1.1 on 2024-09-22 01:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('visiting', '預約參觀選位')], default='預約參觀選位', max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('visit_date_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('comment', models.TextField(blank=True)),
                ('submit_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
