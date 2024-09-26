# Generated by Django 5.1.1 on 2024-09-26 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_new_youtube_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='title',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='new',
            name='youtube_link',
            field=models.URLField(blank=True, max_length=1000),
        ),
    ]