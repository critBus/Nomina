# Generated by Django 4.2.7 on 2024-05-04 02:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nomina", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="salariomensualtotalpagado",
            name="pago_por_subsidios",
        ),
        migrations.RemoveField(
            model_name="salariomensualtotalpagado",
            name="pago_por_utilidades_anuales",
        ),
        migrations.AddField(
            model_name="extracertificadomedico",
            name="pago_mensual",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nomina.salariomensualtotalpagado",
                verbose_name="Pago Mensual",
            ),
        ),
        migrations.AddField(
            model_name="licenciaprenatal",
            name="pago_mensual",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nomina.salariomensualtotalpagado",
                verbose_name="Pago Mensual",
            ),
        ),
        migrations.AddField(
            model_name="pagoporutilidadesanuales",
            name="pago_mensual",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nomina.salariomensualtotalpagado",
                verbose_name="Pago Mensual",
            ),
        ),
        migrations.AddField(
            model_name="prestacionsocial",
            name="pago_mensual",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nomina.salariomensualtotalpagado",
                verbose_name="Pago Mensual",
            ),
        ),
        migrations.AddField(
            model_name="primeralicenciaposnatal",
            name="pago_mensual",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nomina.salariomensualtotalpagado",
                verbose_name="Pago Mensual",
            ),
        ),
        migrations.AddField(
            model_name="primercertificadomedico",
            name="pago_mensual",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nomina.salariomensualtotalpagado",
                verbose_name="Pago Mensual",
            ),
        ),
        migrations.AddField(
            model_name="segundalicenciaposnatal",
            name="pago_mensual",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nomina.salariomensualtotalpagado",
                verbose_name="Pago Mensual",
            ),
        ),
    ]