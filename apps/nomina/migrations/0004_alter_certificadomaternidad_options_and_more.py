# Generated by Django 4.2.7 on 2024-04-25 22:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nomina", "0003_alter_escala_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="certificadomaternidad",
            options={
                "verbose_name": "Certificado Maternidad",
                "verbose_name_plural": "Certificados de Maternidad",
            },
        ),
        migrations.AlterField(
            model_name="asistencia",
            name="horas_trabajadas",
            field=models.IntegerField(
                default=8,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(9),
                ],
                verbose_name="Horas Trabajadas",
            ),
        ),
    ]
