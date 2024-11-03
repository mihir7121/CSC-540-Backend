# Generated by Django 5.1.2 on 2024-11-03 03:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0002_remove_content_id_content_content_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('activity_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('hidden', models.BooleanField()),
                ('content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zybooks.content')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='zybooks.question')),
            ],
        ),
    ]