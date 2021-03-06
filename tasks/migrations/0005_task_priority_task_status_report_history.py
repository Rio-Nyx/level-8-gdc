# Generated by Django 4.0.1 on 2022-02-24 16:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0004_task_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="priority",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "PENDING"),
                    ("IN_PROGRESS", "IN_PROGRESS"),
                    ("COMPLETED", "COMPLETED"),
                    ("CANCELLED", "CANCELLED"),
                ],
                default="PENDING",
                max_length=100,
            ),
        ),
        migrations.CreateModel(
            name="Report",
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
                ("send_time", models.TimeField()),
                (
                    "last_report",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2022, 2, 24, 0, 0, 46, 131190, tzinfo=utc
                        ),
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="History",
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
                ("old_status", models.CharField(max_length=100)),
                ("new_status", models.CharField(max_length=100)),
                ("time", models.DateTimeField(auto_now=True)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tasks.task"
                    ),
                ),
            ],
        ),
    ]
