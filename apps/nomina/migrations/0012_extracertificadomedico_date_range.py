# Generated by Django 4.2.7 on 2024-06-01 01:34

import django.contrib.postgres.fields.ranges
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("nomina", "0011_primercertificadomedico_date_range_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="extracertificadomedico",
            name="date_range",
            field=django.contrib.postgres.fields.ranges.DateRangeField(
                blank=True, db_index=True, null=True
            ),
        ),
    ]
