# Generated by Django 5.1.2 on 2024-11-04 21:58

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chapter",
            fields=[
                ("chapter_id", models.AutoField(primary_key=True, serialize=False)),
                ("chapter_name", models.CharField(max_length=10)),
                ("title", models.CharField(max_length=100)),
                ("hidden", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "course_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "course_token",
                    models.CharField(max_length=7, null=True, unique=True),
                ),
                ("course_name", models.CharField(max_length=100)),
                ("start_date", models.DateField(default=django.utils.timezone.now)),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "course_type",
                    models.CharField(
                        choices=[("active", "Active"), ("evaluation", "Evaluation")],
                        max_length=10,
                    ),
                ),
                ("course_capacity", models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("question_id", models.AutoField(primary_key=True, serialize=False)),
                ("question_name", models.CharField(default=None, max_length=10)),
                ("question_text", models.TextField()),
                ("option_1_text", models.CharField(max_length=255)),
                ("option_1_explanation", models.TextField(blank=True, null=True)),
                ("option_2_text", models.CharField(max_length=255)),
                ("option_2_explanation", models.TextField(blank=True, null=True)),
                ("option_3_text", models.CharField(max_length=255)),
                ("option_3_explanation", models.TextField(blank=True, null=True)),
                ("option_4_text", models.CharField(max_length=255)),
                ("option_4_explanation", models.TextField(blank=True, null=True)),
                ("answer", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "user_id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=128)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "Admin"),
                            ("faculty", "Faculty"),
                            ("ta", "Teaching Assistant"),
                            ("student", "Student"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Content",
            fields=[
                ("content_id", models.AutoField(primary_key=True, serialize=False)),
                ("content_name", models.CharField(max_length=10)),
                (
                    "block_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("text", "Text"),
                            ("image", "Image"),
                            ("activities", "Activities"),
                        ],
                        max_length=10,
                    ),
                ),
                ("text_data", models.TextField(blank=True, null=True)),
                (
                    "image_data",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
                ("hidden", models.BooleanField(blank=True)),
                (
                    "chapter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="zybooks.chapter",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Activity",
            fields=[
                ("activity_id", models.AutoField(primary_key=True, serialize=False)),
                ("activity_number", models.CharField(max_length=20)),
                ("hidden", models.BooleanField()),
                (
                    "content",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="zybooks.content",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="zybooks.question",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                ("section_id", models.AutoField(primary_key=True, serialize=False)),
                ("number", models.CharField(max_length=20)),
                ("title", models.CharField(max_length=100)),
                ("hidden", models.BooleanField()),
                (
                    "chapter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="zybooks.chapter",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="content",
            name="section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="zybooks.section"
            ),
        ),
        migrations.CreateModel(
            name="Textbook",
            fields=[
                (
                    "textbook_id",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=100)),
                (
                    "course",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="zybooks.course",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="section",
            name="textbook",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="zybooks.textbook"
            ),
        ),
        migrations.AddField(
            model_name="content",
            name="textbook",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="zybooks.textbook"
            ),
        ),
        migrations.AddField(
            model_name="chapter",
            name="textbook",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="zybooks.textbook"
            ),
        ),
        migrations.CreateModel(
            name="TA",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "hourly_pay",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=0.0, max_digits=5
                    ),
                ),
                ("hours_per_week", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "associated_faculty",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tas",
                        to="zybooks.user",
                    ),
                ),
                (
                    "ta",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ta_name",
                        to="zybooks.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="zybooks.user"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="course",
            name="faculty",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="course_faculty",
                to="zybooks.user",
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="ta",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="course_ta",
                to="zybooks.user",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="section",
            unique_together={("chapter", "textbook", "number")},
        ),
        migrations.AlterUniqueTogether(
            name="content",
            unique_together={("section", "content_id")},
        ),
        migrations.AlterUniqueTogether(
            name="chapter",
            unique_together={("textbook", "chapter_id")},
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total_activities", models.PositiveIntegerField(default=0)),
                ("total_points", models.PositiveIntegerField(default=0)),
                ("activity_status", models.JSONField(default=list)),
                (
                    "course",
                    models.ForeignKey(
                        default="x",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="zybooks.course",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="zybooks.user"
                    ),
                ),
            ],
            options={
                "unique_together": {("course", "user")},
            },
        ),
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("enrolled", "Enrolled")],
                        default="pending",
                        max_length=10,
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="zybooks.course"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="zybooks.user"
                    ),
                ),
            ],
            options={
                "unique_together": {("student", "course")},
            },
        ),
    ]
