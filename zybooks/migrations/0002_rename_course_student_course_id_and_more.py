# Generated by Django 5.1.2 on 2024-11-04 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("zybooks", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="student",
            old_name="course",
            new_name="course_id",
        ),
        migrations.AlterUniqueTogether(
            name="student",
            unique_together={("course_id", "user")},
        ),
    ]