# Generated by Django 5.1.1 on 2024-10-07 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_alter_contact_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='message',
            new_name='comment',
        ),
    ]