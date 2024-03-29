# Generated by Django 4.0.10 on 2023-08-28 22:17

# Django
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Scan",
            fields=[
                (
                    "hash",
                    models.CharField(
                        editable=False,
                        max_length=30,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="Scan hash",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Creation date/time",
                    ),
                ),
                ("raw_data", models.TextField(verbose_name="Scan RAW data")),
                (
                    "scan_type",
                    models.CharField(
                        choices=[
                            ("invalid", "Invalid scan data"),
                            ("dscan", "D-Scan"),
                            ("fleetcomp", "Fleet composition"),
                            ("chatlist", "Chat list"),
                        ],
                        default="invalid",
                        max_length=9,
                        verbose_name="Scan type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Scan",
                "verbose_name_plural": "Scans",
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="ScanData",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "section",
                    models.CharField(
                        choices=[
                            ("invalid", "Invalid scan data"),
                            ("pilotlist", "Pilot list"),
                            ("corporationlist", "Corporation list"),
                            ("alliancelist", "Alliance list"),
                            ("shiptypes", "Ship types"),
                            ("shiplist", "Ship list"),
                            ("shiplist_on_grid", "Ship list (on grid)"),
                            ("shiplist_off_grid", "Ship list (off grid)"),
                            ("structures_on_grid", "Structures (on grid)"),
                            ("starbases_on_grid", "Starbases (on grid)"),
                            ("deployables_on_grid", "Deployables (on grid)"),
                            ("miscellaneous_on_grid", "Miscellaneous (on grid)"),
                            ("solar_system_information", "System information"),
                            ("fleetcomposition", "Fleet composition"),
                        ],
                        default="invalid",
                        max_length=24,
                        verbose_name="Scan section",
                    ),
                ),
                (
                    "processed_data",
                    models.JSONField(default=dict, verbose_name="Processed scan data"),
                ),
                (
                    "scan",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scan_data",
                        to="aa_intel_tool.scan",
                        verbose_name="Scan",
                    ),
                ),
            ],
            options={
                "verbose_name": "Scan data",
                "verbose_name_plural": "Scan data",
                "default_permissions": (),
                "unique_together": {("scan", "section")},
            },
        ),
    ]
