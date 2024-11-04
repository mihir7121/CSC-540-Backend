# Generated by Django 5.1.2 on 2024-11-04 03:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zybooks", "0002_ta_course_alter_course_ta"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ta",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teaching_assistants",
                to="zybooks.course",
            ),
        ),
    ]