# Generated by Django 5.1.2 on 2024-10-31 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zybooks", "0032_alter_course_course_capacity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="course_token",
            field=models.CharField(max_length=7, null=True, unique=True),
        ),
    ]
