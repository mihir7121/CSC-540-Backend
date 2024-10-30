# Generated by Django 5.1.2 on 2024-10-30 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zybooks', '0026_alter_ta_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='position',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='years_of_experience',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
