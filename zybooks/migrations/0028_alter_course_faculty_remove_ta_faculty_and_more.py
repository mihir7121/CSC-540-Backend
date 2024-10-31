# Generated by Django 5.1.2 on 2024-10-30 23:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0027_alter_faculty_department_alter_faculty_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_faculty', to='zybooks.user'),
        ),
        migrations.RemoveField(
            model_name='ta',
            name='faculty',
        ),
        migrations.AlterField(
            model_name='ta',
            name='associated_faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tas', to='zybooks.user'),
        ),
        migrations.AlterField(
            model_name='course',
            name='ta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_ta', to='zybooks.user'),
        ),
        migrations.DeleteModel(
            name='Faculty',
        ),
    ]