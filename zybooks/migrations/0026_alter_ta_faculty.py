# Generated by Django 5.1.2 on 2024-10-30 23:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0025_remove_ta_user_ta_faculty_ta_ta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ta',
            name='faculty',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faculty_name', to='zybooks.faculty'),
        ),
    ]
