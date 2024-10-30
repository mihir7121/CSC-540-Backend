# Generated by Django 5.1.2 on 2024-10-30 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0016_remove_content_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('option_1_text', models.CharField(max_length=255)),
                ('option_1_explanation', models.TextField(blank=True, null=True)),
                ('option_1_label', models.BooleanField()),
                ('option_2_text', models.CharField(max_length=255)),
                ('option_2_explanation', models.TextField(blank=True, null=True)),
                ('option_2_label', models.BooleanField()),
                ('option_3_text', models.CharField(max_length=255)),
                ('option_3_explanation', models.TextField(blank=True, null=True)),
                ('option_3_label', models.BooleanField()),
                ('option_4_text', models.CharField(max_length=255)),
                ('option_4_explanation', models.TextField(blank=True, null=True)),
                ('option_4_label', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('activity_id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='zybooks.question')),
            ],
        ),
    ]
