# Generated by Django 4.2.7 on 2024-05-03 23:44

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import apps.nomina.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CertificadoMedicoGeneral",
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
                    "fecha_inicio",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha Inicio",
                    ),
                ),
                (
                    "ingresado",
                    models.BooleanField(default=False, verbose_name="Ingresado"),
                ),
                ("descripcion", models.TextField(verbose_name="Descripción")),
                (
                    "salario_anual",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Salario Anual",
                    ),
                ),
            ],
            options={
                "verbose_name": "Certificado Medico",
                "verbose_name_plural": "Certificados Medicos",
            },
        ),
        migrations.CreateModel(
            name="LicenciaMaternidad",
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
                    "fecha_inicio",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha Inicio",
                    ),
                ),
            ],
            options={
                "verbose_name": "Licencia de Maternidad",
                "verbose_name_plural": "Licencias de Maternidad",
            },
        ),
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
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Pago Por Subsidios",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PagoPorUtilidadesAnuales",
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
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Pago Por Utilidades",
                    ),
                ),
                (
                    "pago_extra",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Extra",
                    ),
                ),
                (
                    "dinero_a_repartir",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Dinero a Repartir",
                    ),
                ),
                (
                    "salario_anual",
                    models.DecimalField(
                        decimal_places=2, max_digits=15, verbose_name="Salario Anual"
                    ),
                ),
                (
                    "tiempo_real_trabajado_en_dias",
                    models.IntegerField(
                        default=0, verbose_name="Tiempo Real Trabajado en días "
                    ),
                ),
            ],
            options={
                "verbose_name": "Utilidad Anual",
                "verbose_name_plural": "Utilidades Anuales",
            },
        ),
        migrations.CreateModel(
            name="PlanificacionUtilidadesAnuales",
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
                    "year",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(2010),
                            django.core.validators.MaxValueValidator(2030),
                        ],
                        verbose_name="Año",
                    ),
                ),
                (
                    "dinero_a_repartir",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Dinero a Repartir",
                    ),
                ),
                (
                    "sobrante",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=15,
                        verbose_name="Sobrante",
                    ),
                ),
                (
                    "sobrante_por_trabajador",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Sobrante Por Trabajador",
                    ),
                ),
            ],
            options={
                "verbose_name": "Pago Utilidad Anual",
                "verbose_name_plural": "Pago Utilidades Anuales",
            },
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
                        choices=[
                            ("I", "I"),
                            ("II", "II"),
                            ("III", "III"),
                            ("IV", "IV"),
                            ("V", "V"),
                            ("VI", "VI"),
                        ],
                        max_length=256,
                        verbose_name="Grupo Complejidad",
                    ),
                ),
                (
                    "grupo_escala",
                    models.CharField(
                        choices=[
                            ("I", "I"),
                            ("II", "II"),
                            ("III", "III"),
                            ("IV", "IV"),
                            ("V", "V"),
                            ("VI", "VI"),
                            ("VII", "VII"),
                            ("VIII", "VIII"),
                            ("IX", "IX"),
                            ("X", "X"),
                            ("XI", "XI"),
                            ("XII", "XII"),
                            ("XIII", "XIII"),
                            ("XIV", "XIV"),
                            ("XV", "XV"),
                            ("XVI", "XVI"),
                            ("XVII", "XVII"),
                            ("XVIII", "XVIII"),
                            ("XIX", "XIX"),
                            ("XX", "XX"),
                            ("XXI", "XXI"),
                            ("XXII", "XXII"),
                            ("XXIII", "XXIII"),
                            ("XXIV", "XXIV"),
                            ("XXV", "XXV"),
                        ],
                        max_length=256,
                        verbose_name="Grupo Escala",
                    ),
                ),
                (
                    "rango_salarial_1",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="I",
                    ),
                ),
                (
                    "rango_salarial_2",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="II",
                    ),
                ),
                (
                    "rango_salarial_3",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="III",
                    ),
                ),
                (
                    "rango_salarial_4",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="IV",
                    ),
                ),
                (
                    "rango_salarial_5",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="V",
                    ),
                ),
            ],
            options={
                "verbose_name": "Salario Escala",
                "verbose_name_plural": "Salarios Escala",
            },
        ),
        migrations.CreateModel(
            name="Trabajador",
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
                    "carnet",
                    models.CharField(
                        max_length=11,
                        unique=True,
                        validators=[
                            apps.nomina.models.length_validation_11,
                            django.core.validators.RegexValidator("^[0-9]{11}$"),
                            apps.nomina.models.not_empty_validation,
                        ],
                        verbose_name="Carnet",
                    ),
                ),
                (
                    "nombre",
                    models.CharField(
                        max_length=50,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$"
                            ),
                            apps.nomina.models.not_empty_validation,
                        ],
                        verbose_name="Nombre",
                    ),
                ),
                (
                    "apellidos",
                    models.CharField(
                        max_length=50,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$"
                            ),
                            apps.nomina.models.not_empty_validation,
                        ],
                        verbose_name="Apellidos",
                    ),
                ),
                (
                    "categoria_ocupacional",
                    models.CharField(
                        choices=[
                            ("Categoria1", "Categoria1"),
                            ("Categoria2", "Categoria2"),
                        ],
                        max_length=256,
                        verbose_name="Categoria Ocupacional",
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                (
                    "telefono",
                    models.CharField(
                        max_length=8,
                        unique=True,
                        validators=[
                            apps.nomina.models.length_validation_8,
                            django.core.validators.RegexValidator("^[0-9]{8}$"),
                            apps.nomina.models.not_empty_validation,
                        ],
                        verbose_name="Telefono",
                    ),
                ),
                (
                    "direccion",
                    models.CharField(max_length=256, verbose_name="Dirección"),
                ),
                (
                    "area",
                    models.CharField(
                        choices=[
                            ("Economía", "Economía"),
                            ("Desarrollo", "Desarrollo"),
                            ("Dirección", "Dirección"),
                        ],
                        max_length=256,
                        verbose_name="Área",
                    ),
                ),
                (
                    "salario_escala",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="nomina.salarioescala",
                        verbose_name="Salario Escala",
                    ),
                ),
            ],
            options={
                "verbose_name": "Trabajador",
                "verbose_name_plural": "Trabajadores",
            },
        ),
        migrations.CreateModel(
            name="SegundaLicenciaPosnatal",
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
                    "fecha_inicio",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha Inicio",
                    ),
                ),
                (
                    "fecha_fin",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha fin",
                    ),
                ),
                (
                    "prestacion_economica",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Prestación Económica",
                    ),
                ),
                (
                    "licencia_maternidad",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nomina.licenciamaternidad",
                    ),
                ),
            ],
            options={
                "verbose_name": "Segunda Licencia Posnatal",
                "verbose_name_plural": "Segundas Licencias Posnatal",
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
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Salario Devengado Mensual",
                    ),
                ),
                (
                    "salario_basico_mensual",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Salario Basico Mensual",
                    ),
                ),
                (
                    "evaluacion_obtenida_por_el_jefe",
                    models.CharField(
                        choices=[
                            ("D", "Deficiente"),
                            ("R", "Regular"),
                            ("B", "Bien"),
                            ("MB", "Muy Bien"),
                            ("E", "Excelente"),
                        ],
                        max_length=256,
                        verbose_name="Evaluación",
                    ),
                ),
                (
                    "evaluacion_obtenida_por_el_jefe_en_puntos",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Puntos",
                    ),
                ),
                (
                    "horas_trabajadas",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Horas Trabajadas",
                    ),
                ),
                (
                    "pago_por_dias_feriados",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Pago Dias Feriados",
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
                    "pago_por_utilidades_anuales",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="nomina.pagoporutilidadesanuales",
                        verbose_name="Pago Por Utilidades",
                    ),
                ),
                (
                    "trabajador",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nomina.trabajador",
                        verbose_name="Trabajador",
                    ),
                ),
            ],
            options={
                "verbose_name": "Salario Mensual",
                "verbose_name_plural": "Salarios Mensuales",
            },
        ),
        migrations.CreateModel(
            name="PrimerCertificadoMedico",
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
                    "fecha_inicio",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha Inicio",
                    ),
                ),
                (
                    "fecha_fin",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha fin",
                    ),
                ),
                (
                    "prestacion_economica",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Prestación Económica",
                    ),
                ),
                (
                    "horas_laborales",
                    models.IntegerField(default=0, verbose_name="Horas Laborales"),
                ),
                (
                    "horas_laborales_en_dias_de_carencia",
                    models.IntegerField(default=0, verbose_name="Carencia"),
                ),
                (
                    "certificado_medico_general",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nomina.certificadomedicogeneral",
                    ),
                ),
            ],
            options={
                "verbose_name": "Primer Certificado Medico",
                "verbose_name_plural": "Primer Certificados Medicos",
            },
        ),
        migrations.CreateModel(
            name="PrimeraLicenciaPosnatal",
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
                    "fecha_inicio",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha Inicio",
                    ),
                ),
                (
                    "fecha_fin",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha fin",
                    ),
                ),
                (
                    "prestacion_economica",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Prestación Económica",
                    ),
                ),
                (
                    "licencia_maternidad",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nomina.licenciamaternidad",
                    ),
                ),
            ],
            options={
                "verbose_name": "Primera Licencia Posnatal",
                "verbose_name_plural": "Primeras Licencias Posnatal",
            },
        ),
        migrations.CreateModel(
            name="PrestacionSocial",
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
                    "fecha_inicio",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha Inicio",
                    ),
                ),
                (
                    "fecha_fin",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha fin",
                    ),
                ),
                (
                    "prestacion_economica",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Prestación Económica",
                    ),
                ),
                (
                    "licencia_maternidad",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nomina.licenciamaternidad",
                    ),
                ),
            ],
            options={
                "verbose_name": "Prestación Social",
                "verbose_name_plural": "Prestaciones Sociales",
            },
        ),
        migrations.AddField(
            model_name="pagoporutilidadesanuales",
            name="planificacion",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="nomina.planificacionutilidadesanuales",
                verbose_name="Planificación",
            ),
        ),
        migrations.AddField(
            model_name="pagoporutilidadesanuales",
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
        migrations.CreateModel(
            name="LicenciaPrenatal",
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
                    "fecha_inicio",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha Inicio",
                    ),
                ),
                (
                    "fecha_fin",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha fin",
                    ),
                ),
                ("es_simple", models.BooleanField(default=True)),
                (
                    "prestacion_economica",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Prestación Económica",
                    ),
                ),
                (
                    "importe_semanal",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Prestación Económica",
                    ),
                ),
                (
                    "salario_anual",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Salario Anual",
                    ),
                ),
                (
                    "licencia_maternidad",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nomina.licenciamaternidad",
                    ),
                ),
                (
                    "trabajador",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nomina.trabajador",
                        verbose_name="Trabajador",
                    ),
                ),
            ],
            options={
                "verbose_name": "Licencia Prenatal",
                "verbose_name_plural": "Licencias Prenatales",
            },
        ),
        migrations.AddField(
            model_name="licenciamaternidad",
            name="trabajador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="nomina.trabajador",
                verbose_name="Trabajador",
            ),
        ),
        migrations.CreateModel(
            name="ExtraCertificadoMedico",
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
                    "fecha_inicio",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha Inicio",
                    ),
                ),
                (
                    "fecha_fin",
                    models.DateField(
                        validators=[apps.nomina.models.date_not_old_validation],
                        verbose_name="Fecha fin",
                    ),
                ),
                (
                    "prestacion_economica",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Prestación Económica",
                    ),
                ),
                (
                    "horas_laborales",
                    models.IntegerField(default=0, verbose_name="Horas Laborales"),
                ),
                (
                    "horas_laborales_en_dias_de_carencia",
                    models.IntegerField(default=0, verbose_name="Carencia"),
                ),
                (
                    "certificado_medico_general",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nomina.certificadomedicogeneral",
                    ),
                ),
            ],
            options={
                "verbose_name": "Certificado Medico Extra",
                "verbose_name_plural": "Certificados Medicos Extra",
            },
        ),
        migrations.AddField(
            model_name="certificadomedicogeneral",
            name="trabajador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="nomina.trabajador",
                verbose_name="Trabajador",
            ),
        ),
        migrations.CreateModel(
            name="Asistencia",
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
                        validators=[
                            apps.nomina.models.date_not_old_validation,
                            apps.nomina.models.date_not_future_validation,
                        ],
                        verbose_name="Fecha",
                    ),
                ),
                (
                    "horas_trabajadas",
                    models.IntegerField(
                        default=apps.nomina.models.get_horas_correctas,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(9),
                        ],
                        verbose_name="Horas Trabajadas",
                    ),
                ),
                (
                    "trabajador",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nomina.trabajador",
                        verbose_name="Trabajador",
                    ),
                ),
            ],
            options={
                "verbose_name": "Asistencia",
                "verbose_name_plural": "Asistencias",
                "unique_together": {("trabajador", "fecha")},
            },
        ),
    ]
