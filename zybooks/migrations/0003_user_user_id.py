# Generated by Django 5.1.2 on 2024-10-28 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0002_course_rename_name_user_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.CharField(blank=True, max_length=8, unique=True),
        ),
    ]
