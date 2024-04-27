# Generated by Django 4.2.7 on 2024-04-27 20:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("nomina", "0004_alter_certificadomaternidad_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PagoPorSubsidios",
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
                (
                    "fecha",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="Fecha"
                    ),
                ),
                (
                    "pago",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Pago Por Subsidios",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PagoPorUtilidades",
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
                (
                    "fecha",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="Fecha"
                    ),
                ),
                (
                    "pago",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Pago Por Utilidades",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SalarioEscala",
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
                (
                    "grupo_complejidad",
                    models.CharField(
                        choices=[("I", "I"), ("II", "II")],
                        max_length=256,
                        verbose_name="Cargo",
                    ),
                ),
                (
                    "grupo_escala",
                    models.CharField(
                        choices=[
                            ("II", "II"),
                            ("III", "III"),
                            ("IV", "IV"),
                            ("V", "V"),
                            ("IV", "IV"),
                        ],
                        max_length=256,
                        verbose_name="Cargo",
                    ),
                ),
                (
                    "rango_salarial",
                    models.IntegerField(
                        choices=[
                            (1, "Rango Salarial 1"),
                            (2, "Rango Salarial 2"),
                            (3, "Rango Salarial 3"),
                            (4, "Rango Salarial 4"),
                            (5, "Rango Salarial 5"),
                        ]
                    ),
                ),
                (
                    "salario",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Salario",
                    ),
                ),
            ],
            options={
                "verbose_name": "Salario Escala",
                "verbose_name_plural": "Salarios Escala",
            },
        ),
        migrations.CreateModel(
            name="SalarioMensualTotalPagado",
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
                (
                    "fecha",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="Fecha"
                    ),
                ),
                (
                    "salario_devengado_mensual",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Salario Devengado Mensual",
                    ),
                ),
                (
                    "salario_basico_mensual",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Salario Basico Mensual",
                    ),
                ),
                (
                    "pago_por_subsidios",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="nomina.pagoporsubsidios",
                        verbose_name="Pago Por Subsidios",
                    ),
                ),
                (
                    "pago_por_utilidades",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="nomina.pagoporutilidades",
                        verbose_name="Pago Por Utilidades",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="trabajador",
            name="cargo",
        ),
        migrations.RemoveField(
            model_name="trabajador",
            name="escala",
        ),
        migrations.DeleteModel(
            name="Cargo",
        ),
        migrations.DeleteModel(
            name="Escala",
        ),
        migrations.AddField(
            model_name="salariomensualtotalpagado",
            name="trabajador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="nomina.trabajador",
                verbose_name="Trabajador",
            ),
        ),
        migrations.AddField(
            model_name="pagoporutilidades",
            name="trabajador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="nomina.trabajador",
                verbose_name="Trabajador",
            ),
        ),
        migrations.AddField(
            model_name="pagoporsubsidios",
            name="trabajador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="nomina.trabajador",
                verbose_name="Trabajador",
            ),
        ),
        migrations.AddField(
            model_name="trabajador",
            name="salario_escala",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nomina.salarioescala",
                verbose_name="Salario Escala",
            ),
        ),
    ]
