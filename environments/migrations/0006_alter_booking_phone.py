# Generated by Django 5.1.1 on 2024-09-20 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environments', '0005_alter_booking_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='phone',
            field=models.IntegerField(max_length=50),
        ),
    ]