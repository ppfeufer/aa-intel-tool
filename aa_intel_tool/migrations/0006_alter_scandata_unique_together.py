# Generated by Django 4.0.10 on 2023-08-22 18:41

# Django
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("aa_intel_tool", "0005_alter_scan_options_alter_scandata_options_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="scandata",
            unique_together={("scan", "section")},
        ),
    ]