# Generated by Django 4.1.7 on 2023-08-30 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_transactioncode"),
    ]

    operations = [
        migrations.CreateModel(
            name="TransactionType",
            fields=[
                (
                    "type_id",
                    models.CharField(
                        default="txn-001",
                        max_length=10,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("short_description", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(null=True)),
                (
                    "fee1_mode",
                    models.CharField(
                        choices=[("percentage", "percentage"), ("flat", "flat")],
                        default="percentage",
                        max_length=10,
                    ),
                ),
                ("fee1", models.FloatField(default=0)),
                (
                    "fee2_mode",
                    models.CharField(
                        choices=[("percentage", "percentage"), ("flat", "flat")],
                        default="percentage",
                        max_length=10,
                    ),
                ),
                ("fee2", models.FloatField(default=0)),
                (
                    "fee3_mode",
                    models.CharField(
                        choices=[("percentage", "percentage"), ("flat", "flat")],
                        default="percentage",
                        max_length=10,
                    ),
                ),
                ("fee3", models.FloatField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        default="active",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "cr_acc",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cr_acc",
                        to="main.account",
                    ),
                ),
                (
                    "cr_gl",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cr_gl",
                        to="main.glline",
                    ),
                ),
                (
                    "cr_transaction_code",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cr_txn_code",
                        to="main.transactioncode",
                    ),
                ),
                (
                    "dr_acc",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dr_acc",
                        to="main.account",
                    ),
                ),
                (
                    "dr_gl",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dr_gl",
                        to="main.glline",
                    ),
                ),
                (
                    "dr_transaction_code",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dr_txn_code",
                        to="main.transactioncode",
                    ),
                ),
            ],
        ),
    ]
