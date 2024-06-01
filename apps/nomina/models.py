from datetime import date, timedelta

from django.contrib.postgres.fields import DateRangeField, DateTimeRangeField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.backends.postgresql.psycopg_any import DateRange, DateTimeTZRange
from django.db.models import Q, Sum
from django.utils import timezone

from apps.nomina.utils.utils import mas_de_uno_en_true

from config.utils.utils_fechas import (
    dias_restantes_mes,
    diferencia_semanas_5_a_7,
    es_dia_entresemana,
    es_viernes,
    get_cantidad_de_horas_entre_semana,
    get_days_in_month,
    get_dias_entre_semana,
    get_horas_correctas,
    misma_semana,
    primer_cumpleannos,
    siguiente_dia_seis_semanas,
    veces_supera_siete,
)

NOMBRE_CARGO_DIRECTOR = "Director"
NOMBRE_ROL_ADMINISTRADOR = "Administrador"
NOMBRE_ROL_TRABAJADOR = "Trabajador"


def not_empty_validation(texto):
    if len(str(texto).strip()) == 0:
        raise ValidationError("No puede estar compuesto solo por espacios")


def length_validation_8(texto):
    cantidad_caracteres = 8
    if len(str(texto).strip()) != cantidad_caracteres:
        raise ValidationError(
            f"Tiene que tener exactamente {cantidad_caracteres} caracteres "
        )


def length_validation_11(texto):
    cantidad_caracteres = 11
    if len(str(texto).strip()) != cantidad_caracteres:
        raise ValidationError(
            f"Tiene que tener exactamente {cantidad_caracteres} caracteres "
        )


def date_not_old_validation(fecha):
    minimo = 2000
    if fecha.year < 2000:
        raise ValidationError(f"El año debe ser superior al {minimo}")


def date_not_future_validation(fecha):
    hoy = timezone.now().date()
    if fecha > hoy:
        raise ValidationError("La fecha no puede ser en el futuro")


class DiaFeriado(models.Model):
    class Meta:
        verbose_name = "Día Feriado"
        verbose_name_plural = "Dias Feriados"

    fecha = models.DateField(
        verbose_name="Fecha",
    )
    nombre = models.CharField(
        verbose_name="Nombre",
        max_length=50,
        null=True,
        blank=True,
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.fecha} {self.nombre}"


class SalarioEscala(models.Model):
    class Meta:
        verbose_name = "Salario Escala"
        verbose_name_plural = "Salarios Escala"

    grupo_complejidad = models.CharField(
        verbose_name="Grupo Complejidad",
        max_length=256,
        choices=[
            (
                "I",
                "I",
            ),
            (
                "II",
                "II",
            ),
            (
                "III",
                "III",
            ),
            (
                "IV",
                "IV",
            ),
            (
                "V",
                "V",
            ),
            (
                "VI",
                "VI",
            ),
        ],
    )
    grupo_escala = models.CharField(
        verbose_name="Grupo Escala",
        max_length=256,
        choices=[
            (
                "I",
                "I",
            ),
            (
                "II",
                "II",
            ),
            (
                "III",
                "III",
            ),
            (
                "IV",
                "IV",
            ),
            (
                "V",
                "V",
            ),
            (
                "VI",
                "VI",
            ),
            (
                "VII",
                "VII",
            ),
            (
                "VIII",
                "VIII",
            ),
            (
                "IX",
                "IX",
            ),
            (
                "X",
                "X",
            ),
            (
                "XI",
                "XI",
            ),
            (
                "XII",
                "XII",
            ),
            (
                "XIII",
                "XIII",
            ),
            (
                "XIV",
                "XIV",
            ),
            (
                "XV",
                "XV",
            ),
            (
                "XVI",
                "XVI",
            ),
            (
                "XVII",
                "XVII",
            ),
            (
                "XVIII",
                "XVIII",
            ),
            (
                "XIX",
                "XIX",
            ),
            (
                "XX",
                "XX",
            ),
            (
                "XXI",
                "XXI",
            ),
            (
                "XXII",
                "XXII",
            ),
            (
                "XXIII",
                "XXIII",
            ),
            (
                "XXIV",
                "XXIV",
            ),
            (
                "XXV",
                "XXV",
            ),
        ],
    )

    rango_salarial_1 = models.IntegerField(
        verbose_name="I",  # "Rango Salarial 1",
        default=0,
        validators=[
            MinValueValidator(0),
        ],
    )
    rango_salarial_2 = models.IntegerField(
        verbose_name="II",  # "Rango Salarial 2",
        default=0,
        validators=[
            MinValueValidator(0),
        ],
    )
    rango_salarial_3 = models.IntegerField(
        verbose_name="III",  # "Rango Salarial 3",
        default=0,
        validators=[
            MinValueValidator(0),
        ],
    )
    rango_salarial_4 = models.IntegerField(
        verbose_name="IV",  # "Rango Salarial 4",
        default=0,
        validators=[
            MinValueValidator(0),
        ],
    )
    rango_salarial_5 = models.IntegerField(
        verbose_name="V",  # "Rango Salarial 5",
        default=0,
        validators=[
            MinValueValidator(0),
        ],
    )

    @property
    def categoria_ocupacional(self):
        if self.grupo_complejidad == "I":
            return "Operario"
        elif self.grupo_complejidad == "II":
            return "Servicios"
        elif self.grupo_complejidad == "III":
            return "Técnicos de actividad o gestion"
        elif self.grupo_complejidad == "IV":
            return "Técnicos gestores de actividad de gestion"
        elif self.grupo_complejidad == "V":
            return "Técnicos actividades generales"
        return "Técnicos gestores actividades principales"

    def __str__(self):
        return f"{self.grupo_complejidad} {self.grupo_escala} "


class Trabajador(models.Model):
    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"

    carnet = models.CharField(
        verbose_name="Carnet",
        unique=True,
        max_length=50,
        validators=[
            length_validation_11,
            RegexValidator(r"^[0-9]{11}$"),
            not_empty_validation,
        ],
    )
    nombre = models.CharField(
        verbose_name="Nombre",
        max_length=50,
        validators=[RegexValidator(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$"), not_empty_validation],
    )
    apellidos = models.CharField(
        verbose_name="Apellidos",
        max_length=50,
        validators=[RegexValidator(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$"), not_empty_validation],
    )
    categoria_ocupacional = models.CharField(
        verbose_name="Categoria Ocupacional",
        max_length=256,
        choices=[
            (
                "Categoria1",
                "Categoria1",
            ),
            (
                "Categoria2",
                "Categoria2",
            ),
        ],
    )
    email = models.EmailField(verbose_name="Email")
    telefono = models.CharField(
        verbose_name="Telefono",
        max_length=8,
        unique=True,
        validators=[
            length_validation_8,
            RegexValidator(r"^[0-9]{8}$"),
            not_empty_validation,
        ],
    )
    cargo = models.CharField(
        verbose_name="Cargo",
        max_length=50,
        validators=[not_empty_validation],
    )
    sexo = models.CharField(
        verbose_name="Sexo",
        max_length=50,
        default="Masculino",
        choices=[("Masculino", "Masculino"), ("Femenino", "Femenino")],
    )
    direccion = models.CharField(verbose_name="Dirección", max_length=256)
    area = models.CharField(
        verbose_name="Área",
        max_length=256,
        choices=[
            (
                "Economía",
                "Economía",
            ),
            (
                "Desarrollo",
                "Desarrollo",
            ),
            (
                "Dirección",
                "Dirección",
            ),
        ],
    )
    salario_escala = models.ForeignKey(
        SalarioEscala,
        on_delete=models.SET_NULL,
        verbose_name="Salario Escala",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Asistencia(models.Model):
    class Meta:
        unique_together = (("trabajador", "fecha"),)
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    fecha = models.DateField(
        verbose_name="Fecha",
        validators=[date_not_old_validation, date_not_future_validation],
    )
    horas_trabajadas = models.IntegerField(
        verbose_name="Horas Trabajadas",
        default=get_horas_correctas,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )
    # es_feriado = models.BooleanField(verbose_name="Feriado",default=False)

    def __str__(self):
        return f"{self.trabajador.nombre} {self.trabajador.apellidos} {self.fecha}"

    # def save(self, *args, **kwargs):
    #     self.es_feriado=es_dia_feriado(self.fecha)
    #     return super().save(*args, **kwargs)


class CertificadoMedicoGeneral(models.Model):
    class Meta:
        verbose_name = "Certificado Medico"
        verbose_name_plural = "Certificados Medicos"

    fecha_inicio = models.DateField(
        verbose_name="Fecha Inicio",
        validators=[date_not_old_validation],
        null=True,
        blank=True,
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )
    ingresado = models.BooleanField(verbose_name="Ingresado", default=False)
    descripcion = models.TextField(
        verbose_name="Descripción",
        null=True,
        blank=True,
    )

    salario_anual = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Salario Anual",
        validators=[MinValueValidator(0)],
        default=0,
    )

    def __str__(self):
        return f"{self.trabajador.nombre} {self.trabajador.apellidos}"


class PrimerCertificadoMedico(models.Model):
    class Meta:
        verbose_name = "Primer Certificado Medico"
        verbose_name_plural = "Primer Certificados Medicos"

    fecha_inicio = models.DateField(
        verbose_name="Fecha Inicio", validators=[date_not_old_validation]
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin", validators=[date_not_old_validation]
    )

    prestacion_economica = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Prestación Económica",
        validators=[MinValueValidator(0)],
        default=0,
    )

    certificado_medico_general = models.OneToOneField(
        CertificadoMedicoGeneral,
        on_delete=models.CASCADE,
    )
    horas_laborales = models.IntegerField(
        verbose_name="Horas Laborales",
        default=0,
    )
    horas_laborales_en_dias_de_carencia = models.IntegerField(
        verbose_name="Carencia",
        default=0,
    )

    pago_mensual = models.ForeignKey(
        "nomina.SalarioMensualTotalPagado",
        on_delete=models.SET_NULL,
        verbose_name="Pago Mensual",
        null=True,
        blank=True,
    )
    date_range = DateRangeField(null=True, blank=True, db_index=True)

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )
            if self.certificado_medico_general:
                se_intercepta(
                    trabajador=self.certificado_medico_general.trabajador, entidad=self
                )

    def __str__(self):
        return f"{self.certificado_medico_general.trabajador.nombre} {self.certificado_medico_general.trabajador.apellidos} {self.fecha_inicio}"

    def calcular_HT(self):
        asistencias = Asistencia.objects.filter(
            trabajador=self.certificado_medico_general.trabajador,
            fecha__year=self.fecha.year,
            fecha__month=self.fecha.month,
        )  # .distinct()

        suma = 0
        for asistencia in asistencias:
            suma += asistencia.horas_trabajadas
        # print(suma)

        return suma

    def actualizar_pago(self):
        self.certificado_medico_general.salario_anual = calcular_SA(
            self.fecha_inicio, self.certificado_medico_general.trabajador
        )
        self.certificado_medico_general.save()
        SA = self.certificado_medico_general.salario_anual
        X = SA / 12
        Y = float(X) / float(190.6)
        if not self.certificado_medico_general.ingresado:
            Z = Y * 60 / 100
        else:
            Z = Y * 50 / 100
        HT = get_cantidad_de_horas_entre_semana(self.fecha_inicio, self.fecha_fin)
        self.horas_laborales = HT

        self.certificado_medico_general.fecha_inicio = self.fecha_inicio
        self.certificado_medico_general.save()
        DC = get_cantidad_de_horas_entre_semana(
            self.fecha_inicio, self.fecha_fin, cantidad_maxima_de_dias=3
        )
        self.horas_laborales_en_dias_de_carencia = DC
        C = Z * (HT - DC)

        self.prestacion_economica = C

    def save(self, *args, **kwargs):
        self.actualizar_pago()
        self.date_range = DateRange(self.fecha_inicio, self.fecha_fin, bounds="[]")
        # self.date_range=(self.fecha_inicio, self.fecha_fin)
        return super().save(*args, **kwargs)


class ExtraCertificadoMedico(models.Model):
    class Meta:
        verbose_name = "Certificado Medico Extra"
        verbose_name_plural = "Certificados Medicos Extra"

    fecha_inicio = models.DateField(
        verbose_name="Fecha Inicio", validators=[date_not_old_validation]
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin", validators=[date_not_old_validation]
    )

    prestacion_economica = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Prestación Económica",
        validators=[MinValueValidator(0)],
        default=0,
    )

    certificado_medico_general = models.ForeignKey(
        CertificadoMedicoGeneral,
        on_delete=models.CASCADE,
    )
    horas_laborales = models.IntegerField(
        verbose_name="Horas Laborales",
        default=0,
    )
    horas_laborales_en_dias_de_carencia = models.IntegerField(
        verbose_name="Carencia",
        default=0,
    )
    pago_mensual = models.ForeignKey(
        "nomina.SalarioMensualTotalPagado",
        on_delete=models.SET_NULL,
        verbose_name="Pago Mensual",
        null=True,
        blank=True,
    )
    date_range = DateRangeField(null=True, blank=True, db_index=True)

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )
            if self.certificado_medico_general:
                se_intercepta(
                    trabajador=self.certificado_medico_general.trabajador, entidad=self
                )

    def __str__(self):
        return f"{self.certificado_medico_general.trabajador.nombre} {self.certificado_medico_general.trabajador.apellidos} {self.fecha_inicio}"

    def calcular_HT(self):
        asistencias = Asistencia.objects.filter(
            trabajador=self.certificado_medico_general.trabajador,
            fecha__year=self.fecha.year,
            fecha__month=self.fecha.month,
        )  # .distinct()

        suma = 0
        for asistencia in asistencias:
            suma += asistencia.horas_trabajadas
        # print(suma)

        return suma

    def actualizar_pago(self):
        primer_certificado: PrimerCertificadoMedico = (
            PrimerCertificadoMedico.objects.filter(
                certificado_medico_general=self.certificado_medico_general
            ).first()
        )
        if self.certificado_medico_general.salario_anual == 0:
            fecha_incio = self.fecha_inicio
            if primer_certificado:
                fecha_incio = primer_certificado.fecha_inicio
            self.certificado_medico_general.salario_anual = calcular_SA(
                fecha_incio, self.certificado_medico_general.trabajador
            )
            self.certificado_medico_general.save()
        SA = self.certificado_medico_general.salario_anual
        X = SA / 12
        Y = float(X) / float(190.6)
        if not self.certificado_medico_general.ingresado:
            Z = Y * 60 / 100
        else:
            Z = Y * 50 / 100
        HT = get_cantidad_de_horas_entre_semana(self.fecha_inicio, self.fecha_fin)
        self.horas_laborales = HT

        C = Z * HT

        self.prestacion_economica = C

    def save(self, *args, **kwargs):
        self.actualizar_pago()
        self.date_range = DateRange(self.fecha_inicio, self.fecha_fin, bounds="[]")
        return super().save(*args, **kwargs)


class LicenciaMaternidad(models.Model):
    class Meta:
        verbose_name = "Licencia de Maternidad"
        verbose_name_plural = "Licencias de Maternidad"

    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )

    fecha_inicio = models.DateField(
        verbose_name="Fecha Inicio", validators=[date_not_old_validation]
    )

    def clean(self):
        super().clean()
        if self.trabajador.sexo != "Femenino":
            raise ValidationError("El trabajador debe de ser una mujer")

    def __str__(self):
        return f"{self.trabajador.nombre} {self.trabajador.apellidos}"


class LicenciaPrenatal(models.Model):
    class Meta:
        verbose_name = "Licencia Prenatal"
        verbose_name_plural = "Licencias Prenatales"

    fecha_inicio = models.DateField(
        verbose_name="Fecha Inicio", validators=[date_not_old_validation]
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin", validators=[date_not_old_validation]
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )
    licencia_maternidad = models.OneToOneField(
        LicenciaMaternidad,
        on_delete=models.CASCADE,
    )
    es_simple = models.BooleanField(default=True)

    prestacion_economica = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Prestación Económica",
        validators=[MinValueValidator(0)],
        default=0,
    )
    importe_semanal = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Importe Semanal",
        validators=[MinValueValidator(0)],
    )
    salario_anual = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Salario Anual",
        validators=[MinValueValidator(0)],
    )
    pago_mensual = models.ForeignKey(
        "nomina.SalarioMensualTotalPagado",
        on_delete=models.SET_NULL,
        verbose_name="Pago Mensual",
        null=True,
        blank=True,
    )
    date_range = DateRangeField(null=True, blank=True, db_index=True)

    def clean(self):
        super().clean()
        if self.fecha_inicio and self.fecha_fin:
            se_intercepta(trabajador=self.trabajador, entidad=self)

    def __str__(self):
        return (
            f"{self.trabajador.nombre} {self.trabajador.apellidos} {self.fecha_inicio}"
        )

    def calcular_fecha_fin(self):
        siguiente_dia = siguiente_dia_seis_semanas(self.fecha_inicio)
        self.fecha_fin = siguiente_dia_laborable(siguiente_dia, incluir_este_dia=True)

    def save(self, *args, **kwargs):
        # nombre_dia_semana(self.fecha_inicio)
        fecha_de_inicio_del_embarazo = self.fecha_inicio
        self.salario_anual = calcular_SA(
            fecha=fecha_de_inicio_del_embarazo, trabajador=self.trabajador
        )
        ISP = (
            self.salario_anual / 52
        )  # calcular_ISP(fecha=fecha_de_inicio_del_embarazo,trabajador=self.trabajador )
        self.importe_semanal = ISP
        self.prestacion_economica = ISP * 6 if self.es_simple else ISP * 8
        self.calcular_fecha_fin()

        self.date_range = DateRange(self.fecha_inicio, self.fecha_fin, bounds="[]")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        PrimeraLicenciaPosnatal.objects.filter(
            licencia_maternidad=self.licencia_maternidad
        ).delete()
        SegundaLicenciaPosnatal.objects.filter(
            licencia_maternidad=self.licencia_maternidad
        ).delete()
        PrestacionSocial.objects.filter(
            licencia_maternidad=self.licencia_maternidad
        ).delete()
        return super().delete(*args, **kwargs)


class PrimeraLicenciaPosnatal(models.Model):
    class Meta:
        verbose_name = "Primera Licencia Posnatal"
        verbose_name_plural = "Primeras Licencias Posnatal"

    fecha_inicio = models.DateField(
        verbose_name="Fecha Inicio", validators=[date_not_old_validation]
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin", validators=[date_not_old_validation]
    )

    prestacion_economica = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Prestación Económica",
        validators=[MinValueValidator(0)],
        default=0,
    )
    licencia_maternidad = models.OneToOneField(
        LicenciaMaternidad,
        on_delete=models.CASCADE,
    )
    pago_mensual = models.ForeignKey(
        "nomina.SalarioMensualTotalPagado",
        on_delete=models.SET_NULL,
        verbose_name="Pago Mensual",
        null=True,
        blank=True,
    )
    date_range = DateRangeField(null=True, blank=True, db_index=True)

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )
            if self.licencia_maternidad:
                se_intercepta(
                    trabajador=self.licencia_maternidad.trabajador, entidad=self
                )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        fecha_de_inicio_del_embarazo = self.fecha_inicio
        if self.licencia_maternidad:
            licencia_prenatal = self.licencia_maternidad.licenciaprenatal
            if licencia_prenatal:
                ISP = (
                    licencia_prenatal.importe_semanal
                )  # calcular_ISP(fecha=fecha_de_inicio_del_embarazo,trabajador=self.licencia_prenatal.trabajador )

                fecha_fin_del_embarazo_real = self.fecha_inicio
                supuesta_fecha_fin_del_embarazo = licencia_prenatal.fecha_fin
                diferencia = 0
                if (
                    fecha_fin_del_embarazo_real != supuesta_fecha_fin_del_embarazo
                    and not misma_semana(
                        fecha_fin_del_embarazo_real, supuesta_fecha_fin_del_embarazo
                    )
                ):
                    cantidad_de_dias_de_diferencia = get_dias_entre_semana(
                        fecha_fin_del_embarazo_real, supuesta_fecha_fin_del_embarazo
                    )
                    cantidad_de_semanas_laborables = veces_supera_siete(
                        cantidad_de_dias_de_diferencia
                    )
                    se_adelanto = cantidad_de_dias_de_diferencia < 0
                    diferencia = cantidad_de_semanas_laborables
                    if se_adelanto:
                        diferencia *= -1
                self.prestacion_economica = (
                    ISP * (6 + diferencia)
                    if licencia_prenatal.es_simple
                    else ISP * (8 + diferencia)
                )
        response = super().save(*args, **kwargs)
        crear_SegundaLicenciaPosnatal(
            self,
            SegundaLicenciaPosnatal.objects.filter(
                licencia_maternidad=self.licencia_maternidad
            ).first()
            if not es_nuevo
            else None,
        )
        self.date_range = DateRange(self.fecha_inicio, self.fecha_fin, bounds="[]")
        return response

    def delete(self, *args, **kwargs):
        SegundaLicenciaPosnatal.objects.filter(
            licencia_maternidad=self.licencia_maternidad
        ).delete()
        PrestacionSocial.objects.filter(
            licencia_maternidad=self.licencia_maternidad
        ).delete()
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.licencia_maternidad.trabajador.nombre}"


class SegundaLicenciaPosnatal(models.Model):
    class Meta:
        verbose_name = "Segunda Licencia Posnatal"
        verbose_name_plural = "Segundas Licencias Posnatal"

    fecha_inicio = models.DateField(
        verbose_name="Fecha Inicio", validators=[date_not_old_validation]
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin", validators=[date_not_old_validation]
    )

    prestacion_economica = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Prestación Económica",
        validators=[MinValueValidator(0)],
        default=0,
    )
    licencia_maternidad = models.OneToOneField(
        LicenciaMaternidad,
        on_delete=models.CASCADE,
    )
    pago_mensual = models.ForeignKey(
        "nomina.SalarioMensualTotalPagado",
        on_delete=models.SET_NULL,
        verbose_name="Pago Mensual",
        null=True,
        blank=True,
    )
    date_range = DateRangeField(null=True, blank=True, db_index=True)

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )
            if self.licencia_maternidad:
                se_intercepta(
                    trabajador=self.licencia_maternidad.trabajador, entidad=self
                )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        if self.licencia_maternidad:
            licencia_prenatal = self.licencia_maternidad.licenciaprenatal
            if licencia_prenatal:
                self.prestacion_economica = licencia_prenatal.prestacion_economica
        response = super().save(*args, **kwargs)

        crear_PrestacionSocial(
            self,
            PrestacionSocial.objects.filter(
                licencia_maternidad=self.licencia_maternidad
            ).first()
            if not es_nuevo
            else None,
        )
        self.date_range = DateRange(self.fecha_inicio, self.fecha_fin, bounds="[]")
        return response

    def __str__(self):
        return f"{self.licencia_maternidad.trabajador.nombre}"


def crear_SegundaLicenciaPosnatal(primera: PrimeraLicenciaPosnatal, segunda=None):
    if not segunda:
        segunda = SegundaLicenciaPosnatal()
    segunda.fecha_inicio = siguiente_dia_laborable(primera.fecha_fin)
    licencia_maternidad = primera.licencia_maternidad
    if licencia_maternidad:
        segunda.licencia_maternidad = licencia_maternidad
        licencia_prenatal = licencia_maternidad.licenciaprenatal
        if licencia_prenatal:
            cantidad_semanas = 6 if licencia_prenatal.es_simple else 8
            segunda.fecha_fin = segunda.fecha_inicio + timedelta(weeks=cantidad_semanas)
    # segunda.primera_licencia_posnatal = primera
    segunda.save()


class PrestacionSocial(models.Model):
    class Meta:
        verbose_name = "Prestación Social"
        verbose_name_plural = "Prestaciones Sociales"

    fecha_inicio = models.DateField(
        verbose_name="Fecha Inicio", validators=[date_not_old_validation]
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin", validators=[date_not_old_validation]
    )

    prestacion_economica = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Prestación Económica",
        validators=[MinValueValidator(0)],
        default=0,
    )
    licencia_maternidad = models.OneToOneField(
        LicenciaMaternidad,
        on_delete=models.CASCADE,
    )
    pago_mensual = models.ForeignKey(
        "nomina.SalarioMensualTotalPagado",
        on_delete=models.SET_NULL,
        verbose_name="Pago Mensual",
        null=True,
        blank=True,
    )
    date_range = DateRangeField(null=True, blank=True, db_index=True)

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )
            if self.licencia_maternidad:
                se_intercepta(
                    trabajador=self.licencia_maternidad.trabajador, entidad=self
                )

    def save(self, *args, **kwargs):
        cantidad_de_dias = dias_restantes_mes(self.fecha_inicio)
        if self.licencia_maternidad:
            licencia_prenatal = self.licencia_maternidad.licenciaprenatal
            if licencia_prenatal:
                SA = licencia_prenatal.salario_anual
                PM = (SA / 12) * 60 / 100
                self.prestacion_economica = 12 * PM
                if not cantidad_de_dias > 24:
                    PD = (PM / 24) * 60 / 100
                    self.prestacion_economica += cantidad_de_dias * PD
        self.date_range = DateRange(self.fecha_inicio, self.fecha_fin, bounds="[]")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.licencia_maternidad.trabajador.nombre}"


def crear_PrestacionSocial(segunda: SegundaLicenciaPosnatal, prestacion=None):
    if not prestacion:
        prestacion = PrestacionSocial()
    prestacion.fecha_inicio = siguiente_dia_laborable(segunda.fecha_fin)
    licencia_maternidad = segunda.licencia_maternidad
    if licencia_maternidad:
        primera_licencia_posnatal = licencia_maternidad.primeralicenciaposnatal
        if primera_licencia_posnatal:
            prestacion.fecha_fin = primer_cumpleannos(
                primera_licencia_posnatal.fecha_inicio
            )
        prestacion.licencia_maternidad = licencia_maternidad
    prestacion.save()


class PlanificacionUtilidadesAnuales(models.Model):
    class Meta:
        verbose_name = "Pago Utilidad Anual"
        verbose_name_plural = "Pago Utilidades Anuales"

    fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    year = models.IntegerField(
        verbose_name="Año",
        default=0,
        validators=[MinValueValidator(2010), MaxValueValidator(2030)],
    )
    dinero_a_repartir = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Dinero a Repartir",
        default=0,
        validators=[MinValueValidator(0)],
    )
    sobrante = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Sobrante",
        default=0,
    )
    sobrante_por_trabajador = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Sobrante Por Trabajador",
        default=0,
        validators=[MinValueValidator(0)],
    )

    def crear_utlidades_para_los_trabajadores(self, es_nuevo):
        dinero_a_repartir = self.dinero_a_repartir
        dinero_que_queda = dinero_a_repartir
        fecha_pago_utlidades = self.fecha
        lista_utilidades = []
        trabajadores = Trabajador.objects.all()
        for i, trabajador in enumerate(trabajadores):
            if es_nuevo:
                utilidad = PagoPorUtilidadesAnuales()
            else:
                utilidad = PagoPorUtilidadesAnuales.objects.filter(
                    planificacion=self, trabajador=trabajador
                ).first()
                if not utilidad:
                    utilidad = PagoPorUtilidadesAnuales()
            utilidad.fecha = fecha_pago_utlidades
            utilidad.trabajador = trabajador
            utilidad.dinero_a_repartir = dinero_a_repartir
            utilidad.planificacion = self
            utilidad.calcular_pago()
            if (
                utilidad.tiempo_real_trabajado_en_dias > 0
                and utilidad.salario_anual > 0
            ):
                utilidad.save()
                if (dinero_que_queda - utilidad.pago) < 0:
                    print("dinero insuficiente")
                    break
                dinero_que_queda -= utilidad.pago

                lista_utilidades.append(utilidad)
        self.sobrante = dinero_que_queda
        if dinero_que_queda > 0:
            pago_extra = dinero_que_queda / len(lista_utilidades)
            self.sobrante_por_trabajador = pago_extra
            for i, utilidad in enumerate(lista_utilidades):
                utilidad.pago_extra = pago_extra
                utilidad.save()
        PagoPorUtilidadesAnuales.objects.filter(planificacion=self).exclude(
            id__in=[v.id for v in lista_utilidades]
        ).delete()

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        response = super().save(*args, **kwargs)
        self.crear_utlidades_para_los_trabajadores(es_nuevo)
        return super().save(*args, **kwargs)


class PagoPorUtilidadesAnuales(models.Model):
    class Meta:
        verbose_name = "Utilidad Anual"
        verbose_name_plural = "Utilidades Anuales"

    fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    pago = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Pago Por Utilidades",
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
    pago_extra = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Extra",
        default=0,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )
    planificacion = models.ForeignKey(
        PlanificacionUtilidadesAnuales,
        on_delete=models.CASCADE,
        verbose_name="Planificación",
    )
    dinero_a_repartir = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Dinero a Repartir",
        default=0,
        validators=[MinValueValidator(0)],
    )
    salario_anual = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Salario Anual",
    )
    tiempo_real_trabajado_en_dias = models.IntegerField(
        verbose_name="Tiempo Real Trabajado en días ", default=0
    )
    pago_mensual = models.ForeignKey(
        "nomina.SalarioMensualTotalPagado",
        on_delete=models.SET_NULL,
        verbose_name="Pago Mensual",
        null=True,
        blank=True,
    )

    def calcular_TRT(self, inicio, fin):
        # print(inicio)
        # print(fin)
        return Asistencia.objects.filter(
            fecha__gte=inicio,
            fecha__lte=fin,
            horas_trabajadas__gt=0,
            trabajador=self.trabajador,
        ).count()

    def calcular_pago(self):
        year = self.planificacion.year
        fin = self.fecha.replace(year=year, month=12, day=31)
        inicio = self.fecha.replace(year=year, month=1, day=1)
        self.salario_anual = calcular_SA(fecha=fin, trabajador=self.trabajador)
        SA = self.salario_anual
        self.tiempo_real_trabajado_en_dias = self.calcular_TRT(
            inicio, fin
        )  # get_cantidad_dias_entre_semana(inicio, fin)
        TRT = self.tiempo_real_trabajado_en_dias
        # print(f"TRT {TRT}")

        P = SA / 12
        if P == 0 or TRT == 0:
            print(f"SA {SA} TRT {TRT}")
            self.pago = 0
            return
        O = self.dinero_a_repartir
        K = SA / TRT
        L = O / P
        UA = K * L
        self.pago = UA

    # def save(self, *args, **kwargs):
    #     self.calcular_pago()
    #     return super().save(*args, **kwargs)


# class PagoPorSubsidios(models.Model):
#     fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
#     pago = models.DecimalField(
#         decimal_places=2,
#         max_digits=15,
#         verbose_name="Pago Por Subsidios",
#         validators=[MinValueValidator(0)],
#     )
#     trabajador = models.ForeignKey(
#         Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
#     )


class SalarioMensualTotalPagado(models.Model):
    class Meta:
        verbose_name = "Salario Mensual"
        verbose_name_plural = "Salarios Mensuales"

    EVALUACIONES = [
        (
            "D",
            "Deficiente",
        ),
        (
            "R",
            "Regular",
        ),
        (
            "B",
            "Bien",
        ),
        (
            "MB",
            "Muy Bien",
        ),
        (
            "E",
            "Excelente",
        ),
    ]
    fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    trabajador = models.ForeignKey(
        Trabajador,
        on_delete=models.CASCADE,
        verbose_name="Trabajador",
        blank=True,
        null=True,
    )
    salario_devengado_mensual = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Salario Devengado Mensual",
        validators=[MinValueValidator(0)],
        default=0,
    )
    salario_basico_mensual = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Salario Basico Mensual",
        validators=[MinValueValidator(0)],
        default=0,
    )
    evaluacion_obtenida_por_el_jefe = models.CharField(
        verbose_name="Evaluación", max_length=256, choices=EVALUACIONES, default=0
    )
    pago_total = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Pago Total",
        validators=[MinValueValidator(0)],
        default=0,
    )

    evaluacion_obtenida_por_el_jefe_en_puntos = models.IntegerField(
        verbose_name="Puntos", validators=[MinValueValidator(0)], default=0
    )
    horas_trabajadas = models.IntegerField(
        verbose_name="Horas Trabajadas", validators=[MinValueValidator(0)], default=0
    )
    pago_por_dias_feriados = models.DecimalField(
        verbose_name="Pago Dias Feriados",
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        default=0,
    )
    valorar_certificados_medicos = models.BooleanField(
        verbose_name="Valorar Certificados Médicos", default=True
    )
    valorar_certificados_maternidad = models.BooleanField(
        verbose_name="Valorar Certificados Maternidad", default=True
    )
    valorar_utilidades = models.BooleanField(
        verbose_name="Valorar Utilidades", default=True
    )

    pago_certificados_medicos = models.DecimalField(
        verbose_name="Pago Certificados Médicos",
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        default=0,
    )
    pago_certificados_maternidad = models.DecimalField(
        verbose_name="Pago Certificados Maternidad",
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        default=0,
    )
    pago_utilidades = models.DecimalField(
        verbose_name="Pago Utilidades",
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        default=0,
    )

    salario_anual = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Salario Anual",
        validators=[MinValueValidator(0)],
        default=0,
    )
    salario_devengado_semi_anual = models.DecimalField(
        verbose_name="Salario Devengado Semi Anual ",
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        default=0,
    )

    def get_evalucacion_str(self):
        for evaluacion in self.EVALUACIONES:
            if self.evaluacion_obtenida_por_el_jefe == evaluacion[0]:
                return evaluacion[1]
        return ""

    def calcular_cantidad_de_horas_trabajadas_este_mes(self):
        asistencias = Asistencia.objects.filter(
            trabajador=self.trabajador,
            fecha__year=self.fecha.year,
            fecha__month=self.fecha.month,
        )

        suma = 0
        for asistencia in asistencias:
            suma += asistencia.horas_trabajadas

        return suma

    def calcular_pago_cantidad_de_horas_trabajadas_este_mes_feriados(self):
        """si no hay horas reales trabajadas va a retornar 0, no siquiera voy a calcular
        las horas feriadas"""
        suma = 0

        # print(suma)
        dias_feriados = get_dias_feriado(
            year=self.fecha.year, mes_a_buscar=self.fecha.month
        )
        if dias_feriados:
            cantidad_de_horas_trabajadas_en_los_6_meses = (
                calcular_cantidad_de_horas_trabajadas_de_los_ultimos(self.trabajador, 6)
            )
            if cantidad_de_horas_trabajadas_en_los_6_meses == 0:
                return 0
            SDSA = calcular_SDSA(self.fecha, self.trabajador)

            TH = SDSA / cantidad_de_horas_trabajadas_en_los_6_meses
            for dia in dias_feriados:
                viernes = es_viernes(self.fecha.replace(day=dia))
                # print(f"SDSA {SDSA}")
                suma += 9 if not viernes else 8  # len(dias_feriados)*

            suma *= TH
        return suma

    def actualizar_pago(self):
        puntos = self.evaluacion_obtenida_por_el_jefe_en_puntos
        if puntos < 60:
            evaluacion = "D"
        elif puntos >= 60 and puntos <= 79:
            evaluacion = "R"
        elif puntos >= 80 and puntos <= 89:
            evaluacion = "B"
        elif puntos >= 90 and puntos <= 96:
            evaluacion = "B"
        else:
            evaluacion = "E"
        self.evaluacion_obtenida_por_el_jefe = (
            evaluacion  # self.trabajador.salario_escala
        )
        salario_escala = self.trabajador.salario_escala
        if evaluacion == "D":
            salario_basico_seleccionado = salario_escala.rango_salarial_1
        elif evaluacion == "R":
            salario_basico_seleccionado = salario_escala.rango_salarial_2
        elif evaluacion == "B":
            salario_basico_seleccionado = salario_escala.rango_salarial_3
        elif evaluacion == "MB":
            salario_basico_seleccionado = salario_escala.rango_salarial_4
        elif evaluacion == "E":
            salario_basico_seleccionado = salario_escala.rango_salarial_5
        else:
            salario_basico_seleccionado = 0

        self.salario_basico_mensual = salario_basico_seleccionado
        self.horas_trabajadas = self.calcular_cantidad_de_horas_trabajadas_este_mes()
        # if self.horas_trabajadas>
        self.salario_devengado_mensual = salario_basico_seleccionado
        # self.salario_devengado_mensual*= self.evaluacion_obtenida_por_el_jefe_en_puntos / 100
        self.salario_devengado_mensual /= 190.6
        self.salario_devengado_mensual = float(self.salario_devengado_mensual) * float(
            self.horas_trabajadas
        )

        self.pago_por_dias_feriados = (
            self.calcular_pago_cantidad_de_horas_trabajadas_este_mes_feriados()
        )
        self.salario_devengado_mensual += float(self.pago_por_dias_feriados)

        if self.salario_devengado_mensual > 20000:
            print(f"exedio")

        self.pago_total = self.salario_devengado_mensual
        suma = 0

        prestacion_economica = (
            self.buscar_prestacion_economica_PrimerCertificadoMedico()
        )
        suma += prestacion_economica
        self.pago_certificados_medicos = prestacion_economica
        if self.valorar_certificados_medicos:
            self.salario_devengado_mensual = float(
                self.salario_devengado_mensual
            ) - float(prestacion_economica)
        prestacion_economica = self.buscar_prestacion_economica_ExtraCertificadoMedico()
        self.pago_certificados_medicos = float(self.pago_certificados_medicos) + float(
            prestacion_economica
        )
        suma += prestacion_economica
        if self.valorar_certificados_medicos:
            self.salario_devengado_mensual = float(
                self.salario_devengado_mensual
            ) - float(prestacion_economica)
        prestacion_economica = self.buscar_prestacion_economica_LicenciaPrenatal()
        self.pago_certificados_maternidad = prestacion_economica
        suma += prestacion_economica
        if self.valorar_certificados_maternidad:
            self.salario_devengado_mensual = float(
                self.salario_devengado_mensual
            ) - float(prestacion_economica)
        prestacion_economica = (
            self.buscar_prestacion_economica_PrimeraLicenciaPosnatal()
        )
        self.pago_certificados_maternidad = float(
            self.pago_certificados_maternidad
        ) + float(prestacion_economica)
        suma += prestacion_economica
        if self.valorar_certificados_maternidad:
            self.salario_devengado_mensual = float(
                self.salario_devengado_mensual
            ) - float(prestacion_economica)
        prestacion_economica = (
            self.buscar_prestacion_economica_SegundaLicenciaPosnatal()
        )
        self.pago_certificados_maternidad = float(
            self.pago_certificados_maternidad
        ) + float(prestacion_economica)
        suma += prestacion_economica
        if self.valorar_certificados_maternidad:
            self.salario_devengado_mensual = float(
                self.salario_devengado_mensual
            ) - float(prestacion_economica)
        prestacion_economica = self.buscar_prestacion_economica_PrestacionSocial()
        suma += prestacion_economica
        self.pago_certificados_maternidad = float(
            self.pago_certificados_maternidad
        ) + float(prestacion_economica)
        if self.valorar_certificados_maternidad:
            self.salario_devengado_mensual = float(
                self.salario_devengado_mensual
            ) - float(prestacion_economica)
        prestacion_economica = (
            self.buscar_prestacion_economica_PagoPorUtilidadesAnuales()
        )
        suma += prestacion_economica
        self.pago_utilidades = prestacion_economica
        if self.valorar_utilidades:
            self.salario_devengado_mensual = float(
                self.salario_devengado_mensual
            ) - float(prestacion_economica)

        # suma += self.buscar_prestacion_economica(LicenciaPrenatal)
        # suma += self.buscar_prestacion_economica(PrimeraLicenciaPosnatal)
        # suma += self.buscar_prestacion_economica(SegundaLicenciaPosnatal)
        if self.salario_devengado_mensual <= 0:
            self.salario_devengado_mensual = 0

        self.pago_total = float(self.pago_total) + float(suma)

    def buscar_prestacion_economica_PrimerCertificadoMedico(self):
        es_nuevo = self.pk is None

        suma = 0
        if not es_nuevo:
            PrimerCertificadoMedico.objects.filter(
                pago_mensual=self,
            ).exclude(
                Q(
                    fecha_inicio__month=self.fecha.month,
                    fecha_inicio__year=self.fecha.year,
                    certificado_medico_general__trabajador=self.trabajador,
                )
                # | Q(
                #     fecha_fin__month=self.fecha.month,
                #     fecha_fin__year=self.fecha.year,
                #     certificado_medico_general__trabajador=self.trabajador,
                # )
            ).update(pago_mensual=None)

            q = PrimerCertificadoMedico.objects.filter(
                Q(pago_mensual=self)
                | Q(
                    fecha_inicio__month=self.fecha.month,
                    fecha_inicio__year=self.fecha.year,
                    pago_mensual__isnull=True,
                    certificado_medico_general__trabajador=self.trabajador,
                )
                # | Q(
                #     fecha_fin__month=self.fecha.month,
                #     fecha_fin__year=self.fecha.year,
                #     pago_mensual__isnull=True,
                #     certificado_medico_general__trabajador=self.trabajador,
                # )
            )

            # certificados=PrimerCertificadoMedico.objects.filter(pago_mensual=self)
            # print(f" {len(certificados)} m {self.fecha.month} y {self.fecha.year}")
            # for c in certificados:
            #     print(f" {c.fecha_inicio.month} {c.fecha_inicio.year}")
            #
            # certificados = PrimerCertificadoMedico.objects.filter(certificado_medico_general__trabajador=self.trabajador)
            # print(f" {len(certificados)} m {self.fecha.month} y {self.fecha.year}")
            # for c in certificados:
            #     print(f" {c.fecha_inicio.month} {c.fecha_inicio.year} {c.pago_mensual}")
            # print(f"existe {q.exists()}")

        else:
            q = PrimerCertificadoMedico.objects.filter(
                Q(
                    fecha_inicio__month=self.fecha.month,
                    fecha_inicio__year=self.fecha.year,
                    pago_mensual__isnull=True,
                    certificado_medico_general__trabajador=self.trabajador,
                )
                # | Q(
                #     fecha_fin__month=self.fecha.month,
                #     fecha_fin__year=self.fecha.year,
                #     pago_mensual__isnull=True,
                #     certificado_medico_general__trabajador=self.trabajador,
                # )
            )
        q.update(pago_mensual=self)
        suma = q.aggregate(total=Sum("prestacion_economica"))["total"]
        # print(f"suma: {suma}")
        return suma if suma else 0

    def buscar_prestacion_economica_ExtraCertificadoMedico(self):
        es_nuevo = self.pk is None

        suma = 0
        if not es_nuevo:
            ExtraCertificadoMedico.objects.filter(
                pago_mensual=self,
            ).exclude(
                Q(
                    fecha_inicio__month=self.fecha.month,
                    fecha_inicio__year=self.fecha.year,
                    certificado_medico_general__trabajador=self.trabajador,
                )
                | Q(
                    fecha_fin__month=self.fecha.month,
                    fecha_fin__year=self.fecha.year,
                    certificado_medico_general__trabajador=self.trabajador,
                )
            ).update(pago_mensual=None)

            q = ExtraCertificadoMedico.objects.filter(
                Q(pago_mensual=self)
                | Q(
                    fecha_inicio__month=self.fecha.month,
                    fecha_inicio__year=self.fecha.year,
                    pago_mensual__isnull=True,
                    certificado_medico_general__trabajador=self.trabajador,
                )
                | Q(
                    fecha_fin__month=self.fecha.month,
                    fecha_fin__year=self.fecha.year,
                    pago_mensual__isnull=True,
                    certificado_medico_general__trabajador=self.trabajador,
                )
            )

        else:
            q = ExtraCertificadoMedico.objects.filter(
                Q(
                    fecha_inicio__month=self.fecha.month,
                    fecha_inicio__year=self.fecha.year,
                    pago_mensual__isnull=True,
                    certificado_medico_general__trabajador=self.trabajador,
                )
                | Q(
                    fecha_fin__month=self.fecha.month,
                    fecha_fin__year=self.fecha.year,
                    pago_mensual__isnull=True,
                    certificado_medico_general__trabajador=self.trabajador,
                )
            )
        q.update(pago_mensual=self)
        suma = q.aggregate(total=Sum("prestacion_economica"))["total"]
        # print(f"suma: {suma}")
        return suma if suma else 0

    def buscar_prestacion_economica_maternidad(self, clase_modelo):
        es_nuevo = self.pk is None

        suma = 0
        if not es_nuevo:
            clase_modelo.objects.filter(
                pago_mensual=self,
            ).exclude(
                Q(
                    fecha_inicio__month=self.fecha.month,
                    fecha_inicio__year=self.fecha.year,
                    licencia_maternidad__trabajador=self.trabajador,
                )
                # | Q(
                #     fecha_fin__month=self.fecha.month,
                #     fecha_fin__year=self.fecha.year,
                #     licencia_maternidad__trabajador=self.trabajador,
                # )
            ).update(pago_mensual=None)

            q = clase_modelo.objects.filter(
                Q(pago_mensual=self)
                | Q(
                    fecha_inicio__month=self.fecha.month,
                    fecha_inicio__year=self.fecha.year,
                    pago_mensual__isnull=True,
                    licencia_maternidad__trabajador=self.trabajador,
                )
                # | Q(
                #     fecha_fin__month=self.fecha.month,
                #     fecha_fin__year=self.fecha.year,
                #     pago_mensual__isnull=True,
                #     licencia_maternidad__trabajador=self.trabajador,
                # )
            )

        else:
            q = clase_modelo.objects.filter(
                Q(
                    fecha_inicio__month=self.fecha.month,
                    fecha_inicio__year=self.fecha.year,
                    pago_mensual__isnull=True,
                    licencia_maternidad__trabajador=self.trabajador,
                )
                # | Q(
                #     fecha_fin__month=self.fecha.month,
                #     fecha_fin__year=self.fecha.year,
                #     pago_mensual__isnull=True,
                #     licencia_maternidad__trabajador=self.trabajador,
                # )
            )
        q.update(pago_mensual=self)
        suma = q.aggregate(total=Sum("prestacion_economica"))["total"]
        # print(f"suma: {suma}")
        return suma if suma else 0

    def buscar_prestacion_economica_LicenciaPrenatal(
        self,
    ):  # licencia_maternidad__trabajador
        return self.buscar_prestacion_economica_maternidad(LicenciaPrenatal)

    def buscar_prestacion_economica_PrimeraLicenciaPosnatal(self):
        return self.buscar_prestacion_economica_maternidad(PrimeraLicenciaPosnatal)

    def buscar_prestacion_economica_SegundaLicenciaPosnatal(self):
        return self.buscar_prestacion_economica_maternidad(SegundaLicenciaPosnatal)

    def buscar_prestacion_economica_PrestacionSocial(self):
        return self.buscar_prestacion_economica_maternidad(PrestacionSocial)

    def buscar_prestacion_economica_PagoPorUtilidadesAnuales(self):
        es_nuevo = self.pk is None

        suma = 0
        if not es_nuevo:
            PagoPorUtilidadesAnuales.objects.filter(
                pago_mensual=self,
            ).exclude(
                fecha__month=self.fecha.month,
                fecha__year=self.fecha.year,
                trabajador=self.trabajador,
            ).update(pago_mensual=None)

            q = PagoPorUtilidadesAnuales.objects.filter(
                Q(pago_mensual=self)
                | Q(
                    fecha__month=self.fecha.month,
                    fecha__year=self.fecha.year,
                    trabajador=self.trabajador,
                )
            )

        else:
            q = PagoPorUtilidadesAnuales.objects.filter(
                fecha__month=self.fecha.month,
                fecha__year=self.fecha.year,
                trabajador=self.trabajador,
            )
        q.update(pago_mensual=self)
        suma = q.aggregate(total=Sum("pago") + Sum("pago_extra"))["total"]
        # print(f"suma: {suma}")
        return suma if suma else 0

    def actualizar_estadisticas_pagos(self):
        self.salario_devengado_semi_anual = calcular_SDSA(self.fecha, self.trabajador)
        self.salario_anual = calcular_SA(self.fecha, self.trabajador)

    def save(self, *args, **kwargs):
        response = super().save(*args, **kwargs)
        self.actualizar_pago()
        response = super().save(*args, **kwargs)
        self.actualizar_estadisticas_pagos()
        response = super().save(*args, **kwargs)
        return response

    def clean(self):
        super().clean()
        if mas_de_uno_en_true(
            self.valorar_utilidades,
            self.valorar_certificados_medicos,
            self.valorar_certificados_maternidad,
        ):
            raise ValidationError(
                "No se puede valorar mas de una condición al mismo tiempo"
            )

    def __str__(self):
        return f"{self.trabajador.nombre} {self.trabajador.apellidos} {self.fecha}"


def calcular_cantidad_de_horas_trabajadas_de_los_ultimos(trabajador, cantidad_de_meses):
    TH = (
        SalarioMensualTotalPagado.objects.filter(trabajador=trabajador)
        .order_by("-fecha")[:cantidad_de_meses]
        .aggregate(total=Sum("horas_trabajadas"))["total"]
    )
    return TH if TH else 0


def calcular_suma_salario(fecha, trabajador, cantidad_de_meses):
    SA = (
        SalarioMensualTotalPagado.objects.filter(
            fecha__lte=fecha,
            trabajador=trabajador,
        )
        .order_by("-fecha")[:cantidad_de_meses]
        .aggregate(total=Sum("salario_devengado_mensual"))["total"]
    )
    return SA if SA else 0


def calcular_SA(fecha, trabajador):
    return calcular_suma_salario(fecha, trabajador, 12)


def calcular_SDSA(fecha, trabajador):
    return calcular_suma_salario(fecha, trabajador, 6)


def es_dia_feriado(fecha: date):
    return DiaFeriado.objects.filter(fecha=fecha).exists()


def get_dias_feriado(year, mes_a_buscar):
    return [
        v.fecha.day
        for v in DiaFeriado.objects.filter(fecha__year=year, fecha__month=mes_a_buscar)
    ]


def get_dias_laborales(year, month):
    seleccionados = []
    dias = get_days_in_month(year, month)
    for dia in dias:
        if es_dia_entresemana(dia) and not es_dia_feriado(dia):
            seleccionados.append(dia)
    # todos los dias entre semana menos los feriados
    return seleccionados


def get_cantidad_dias_entre_semana(inicio, fin):
    """
    Calcula la cantidad de días entre semana (lunes a viernes) entre dos fechas.

    Args:
        inicio : Fecha de inicio .
        fin : Fecha de fin .

    Returns:
        int: Cantidad de días entre semana entre las dos fechas.
    """

    # Inicializar el contador de días entre semana
    dias_entre_semana = 0

    # Iterar entre las fechas
    current_date = inicio
    while current_date <= fin:
        # Verificar si el día es entre semana (lunes a viernes)
        if current_date.weekday() < 5 and not es_dia_feriado(current_date):
            dias_entre_semana += 1
        # Avanzar al siguiente día
        current_date += timedelta(days=1)

    return dias_entre_semana


def siguiente_dia_laborable(fecha_actual, incluir_este_dia=False):
    siguiente_dia = (
        fecha_actual + timedelta(days=1) if not incluir_este_dia else fecha_actual
    )

    while (not es_dia_entresemana(siguiente_dia)) and not es_dia_feriado(siguiente_dia):
        siguiente_dia += timedelta(days=1)

    return siguiente_dia


def se_intercepta(trabajador, entidad):
    date_range = DateRange(entidad.fecha_inicio, entidad.fecha_fin, bounds="[]")

    es_nuevo = entidad.pk is None

    def comprobar_query_intercepcion(q, mensaje):
        clase = q.model
        if (not es_nuevo) and isinstance(entidad, clase):
            q = q.exclude(pk=entidad.pk)
        if q.exists():
            raise ValidationError(mensaje)

    comprobar_query_intercepcion(
        PrimerCertificadoMedico.objects.filter(
            date_range__overlap=date_range,
            certificado_medico_general__trabajador=trabajador,
        ),
        "Existe otro primer certificado cuyas fechas se interceptan con las actuales",
    )
    comprobar_query_intercepcion(
        ExtraCertificadoMedico.objects.filter(
            date_range__overlap=date_range,
            certificado_medico_general__trabajador=trabajador,
        ),
        "Existe otro certificado cuyas fechas se interceptan con las actuales",
    )
    comprobar_query_intercepcion(
        LicenciaPrenatal.objects.filter(
            date_range__overlap=date_range, trabajador=trabajador
        ),
        "Ya existe una licencia prenatal que se intercepta con estas fechas ",
    )
    comprobar_query_intercepcion(
        PrimeraLicenciaPosnatal.objects.filter(
            date_range__overlap=date_range, licencia_maternidad__trabajador=trabajador
        ),
        "Ya existe una primera licencia posnatal que se intercepta con estas fechas ",
    )
    comprobar_query_intercepcion(
        SegundaLicenciaPosnatal.objects.filter(
            date_range__overlap=date_range, licencia_maternidad__trabajador=trabajador
        ),
        "Ya existe una segunda licencia posnatal que se intercepta con estas fechas ",
    )
    comprobar_query_intercepcion(
        PrestacionSocial.objects.filter(
            date_range__overlap=date_range, licencia_maternidad__trabajador=trabajador
        ),
        "Ya existe una prestacion que se intercepta con estas fechas ",
    )
