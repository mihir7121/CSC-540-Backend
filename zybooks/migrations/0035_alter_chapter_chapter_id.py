# Generated by Django 5.1.2 on 2024-10-31 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zybooks", "0034_alter_course_course_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chapter",
            name="chapter_id",
            field=models.CharField(max_length=7, primary_key=True, serialize=False),
        ),
    ]