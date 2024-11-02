# Generated by Django 5.1.2 on 2024-11-02 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0038_alter_content_content_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zybooks.content'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
