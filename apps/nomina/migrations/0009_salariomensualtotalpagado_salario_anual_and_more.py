# Generated by Django 4.2.7 on 2024-05-16 18:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nomina", "0008_diaferiado_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="salariomensualtotalpagado",
            name="salario_anual",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=15,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Salario Anual",
            ),
        ),
        migrations.AddField(
            model_name="salariomensualtotalpagado",
            name="salario_devengado_semi_anual",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=15,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Salario Devengado Semi Anual ",
            ),
        ),
    ]
