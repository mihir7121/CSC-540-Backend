# Generated by Django 5.1.2 on 2024-10-30 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zybooks", "0023_ta"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ta",
            name="ta_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assigned_tas",
                to="zybooks.user",
            ),
        ),
    ]