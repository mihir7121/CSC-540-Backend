# Generated by Django 5.1.2 on 2024-11-02 22:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0043_remove_content_chapter_remove_content_textbook_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='notification_id',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='read_status',
        ),
        migrations.AddField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='notification',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(),
        ),
    ]
