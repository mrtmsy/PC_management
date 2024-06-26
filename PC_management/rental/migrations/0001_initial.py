# Generated by Django 4.2.1 on 2023-06-30 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("device", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RentalModel",
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
                ("rental_start", models.DateTimeField(verbose_name="貸出日")),
                ("rental_end", models.DateTimeField(null=True, verbose_name="返却日")),
                ("rental_scheduled", models.DateTimeField(verbose_name="返却予定日")),
                ("place", models.CharField(max_length=30, verbose_name="設置場所")),
                (
                    "registration_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="登録日"),
                ),
                (
                    "update_date",
                    models.DateTimeField(auto_now=True, verbose_name="更新日"),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, max_length=200, null=True, verbose_name="備考"
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="削除フラグ"),
                ),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="device.devicemodel",
                        verbose_name="資産番号",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.usersmodel",
                        verbose_name="社員番号",
                    ),
                ),
            ],
        ),
    ]
