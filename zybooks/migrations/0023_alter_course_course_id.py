# Generated by Django 5.1.2 on 2024-10-30 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0022_activity_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
