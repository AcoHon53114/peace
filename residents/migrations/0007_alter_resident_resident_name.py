# Generated by Django 5.1.1 on 2024-10-03 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0006_alter_resident_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='resident_name',
            field=models.CharField(max_length=50),
        ),
    ]
