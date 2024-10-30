# Generated by Django 5.1.2 on 2024-10-30 18:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0022_activity_hidden'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='user',
        ),
        migrations.AddField(
            model_name='course',
            name='user_faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='faculty', to='zybooks.user'),
        ),
        migrations.AddField(
            model_name='course',
            name='user_ta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='TA', to='zybooks.user'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
