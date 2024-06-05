# Generated by Django 5.0.6 on 2024-06-05 14:35

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DB",
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
                ("name", models.CharField(max_length=254)),
                ("db_host", models.CharField(max_length=255)),
                ("db_port", models.IntegerField()),
                ("db_root", models.CharField(max_length=255)),
                ("root_pw", models.CharField(max_length=255)),
                ("secret_key", models.BinaryField()),
                ("salt", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("revocation_id", models.BinaryField()),
                ("url_id", models.UUIDField()),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DBUser",
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
                ("username", models.CharField(max_length=255)),
                ("password", models.CharField(max_length=512)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("active", models.BooleanField(default=True)),
                ("fernet", models.BinaryField()),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Token",
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
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                ("fernet", models.BinaryField()),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserTemp",
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
                ("added_at", models.DateTimeField(auto_now_add=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "db",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Settings.db"
                    ),
                ),
                (
                    "db_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Settings.dbuser",
                    ),
                ),
            ],
        ),
    ]