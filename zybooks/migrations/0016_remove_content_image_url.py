# Generated by Django 5.1.2 on 2024-10-30 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0015_content_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='image_url',
        ),
    ]