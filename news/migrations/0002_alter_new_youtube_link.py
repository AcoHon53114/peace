# Generated by Django 5.1.1 on 2024-09-19 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='youtube_link',
            field=models.URLField(max_length=300),
        ),
    ]
