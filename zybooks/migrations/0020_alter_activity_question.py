# Generated by Django 5.1.2 on 2024-10-30 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0019_alter_question_question_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='zybooks.question'),
        ),
    ]
