# Generated by Django 4.1.7 on 2023-08-28 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_accounttype"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "account_number",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "account_description",
                    models.CharField(
                        blank=True, editable=False, max_length=100, null=True
                    ),
                ),
                ("opening_balance", models.FloatField(default=0)),
                ("current_cleared_balance", models.FloatField(default=0)),
                ("current_uncleared_balance", models.FloatField(default=0)),
                ("total_balance", models.FloatField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "account_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.accounttype",
                    ),
                ),
                (
                    "gl_line_number",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gl_line_number",
                        to="main.glline",
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
            name="AccountEntry",
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
                ("entry_ID", models.CharField(max_length=50, unique=True)),
                (
                    "entry_type",
                    models.CharField(
                        blank=True,
                        choices=[("PL", "PL"), ("AL", "AL")],
                        max_length=2,
                        null=True,
                    ),
                ),
                ("transaction_ID", models.CharField(max_length=100)),
                ("amount", models.FloatField()),
                ("currency", models.CharField(default="KES", max_length=10)),
                ("debit_credit_marker", models.CharField(max_length=100)),
                ("exposure_date", models.DateTimeField(auto_now_add=True)),
                ("entry_date", models.DateTimeField(auto_now_add=True)),
                (
                    "posting_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "account_number",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trustee_acc_number",
                        to="main.account",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
