from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone

# from apps.nomina.utils.util import es_dia_feriado, get_dias_feriado
from apps.nomina.utils.util_salario import (
    get_dias_entre_semana,
    veces_supera_siete,
    misma_semana,
    dias_restantes_mes,
    siguiente_dia_laborable,
    primer_cumpleannos,
    diferencia_menos_de_5_meses, nombre_dia_semana, es_viernes, get_dias_feriado,
)


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
        verbose_name="I",#"Rango Salarial 1",
        default=0,
        validators=[MinValueValidator(0), ],
    )
    rango_salarial_2 = models.IntegerField(
        verbose_name="II",#"Rango Salarial 2",
        default=0,
        validators=[MinValueValidator(0), ],
    )
    rango_salarial_3 = models.IntegerField(
        verbose_name="III",#"Rango Salarial 3",
        default=0,
        validators=[MinValueValidator(0), ],
    )
    rango_salarial_4 = models.IntegerField(
        verbose_name="IV",#"Rango Salarial 4",
        default=0,
        validators=[MinValueValidator(0), ],
    )
    rango_salarial_5 = models.IntegerField(
        verbose_name="V",#"Rango Salarial 5",
        default=0,
        validators=[MinValueValidator(0), ],
    )
    # rango_salarial = models.IntegerField(
    #     choices=(
    #         (1, "Rango Salarial 1"),
    #         (2, "Rango Salarial 2"),
    #         (3, "Rango Salarial 3"),
    #         (4, "Rango Salarial 4"),
    #         (5, "Rango Salarial 5"),
    #     )
    # )

    # salario = models.FloatField(
    #     verbose_name="Salario", validators=[MinValueValidator(0)]
    # )

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
        max_length=11,
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
    # escala = models.ForeignKey(Escala, on_delete=models.CASCADE, verbose_name="Escala")
    # cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name="Cargo")

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

def get_horas_correctas():
    return 8 if es_viernes(timezone.now()) else 9
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

class CertificadoMedico(models.Model):
    class Meta:
        unique_together = (
            (
                "trabajador",
                "fecha_inicio",
            ),
        )
        verbose_name = "Certificado Medico"
        verbose_name_plural = "Certificados Medicos"

    fecha_inicio = models.DateField(
        verbose_name="Fecha Inicio", validators=[date_not_old_validation]
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin", validators=[date_not_old_validation]
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )

    def __str__(self):
        return (
            f"{self.trabajador.nombre} {self.trabajador.apellidos} {self.fecha_inicio}"
        )


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



    def __str__(self):
        return f"{self.trabajador.nombre} {self.trabajador.apellidos}"




class LicenciaPrenatal(models.Model):
    class Meta:
        # unique_together = (
        #     (
        #         "trabajador",
        #         "fecha_inicio",
        #     ),
        # )
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

    prestacion_economica = models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Prestación Económica", validators=[MinValueValidator(0)]
    )
    importe_semanal = models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Prestación Económica", validators=[MinValueValidator(0)]
    )
    salario_anual = models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Salario Anual", validators=[MinValueValidator(0)]
    )

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )
            # if diferencia_menos_de_5_meses(self.fecha_inicio, self.fecha_fin):
            #     raise ValidationError(
            #         "Tiene que existir una distancia lógica entre ambas fechas"
            #     )

    def __str__(self):
        return (
            f"{self.trabajador.nombre} {self.trabajador.apellidos} {self.fecha_inicio}"
        )

    def save(self, *args, **kwargs):
        #nombre_dia_semana(self.fecha_inicio)
        fecha_de_inicio_del_embarazo = self.fecha_inicio
        self.salario_anual = calcular_SA(
            fecha=fecha_de_inicio_del_embarazo, trabajador=self.trabajador
        )
        ISP = (
            self.salario_anual / 52
        )  # calcular_ISP(fecha=fecha_de_inicio_del_embarazo,trabajador=self.trabajador )
        self.importe_semanal = ISP
        self.prestacion_economica = ISP * 6 if self.es_simple else ISP * 8
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        PrimeraLicenciaPosnatal.objects.filter(licencia_maternidad=self.licencia_maternidad).delete()
        SegundaLicenciaPosnatal.objects.filter(licencia_maternidad=self.licencia_maternidad).delete()
        PrestacionSocial.objects.filter(licencia_maternidad=self.licencia_maternidad).delete()
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

    # licencia_prenatal = models.OneToOneField(
    #     LicenciaPrenatal,
    #     on_delete=models.CASCADE,
    #     verbose_name="Licencia Prenatal",
    #
    # )
    prestacion_economica = models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Prestación Económica",
        validators=[MinValueValidator(0)],

    )
    licencia_maternidad = models.OneToOneField(
        LicenciaMaternidad,
        on_delete=models.CASCADE,
    )

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )

            # if self.licencia_maternidad and self.licencia_maternidad.licenciaprenatal:
            #     licencia_prenatal=self.licencia_maternidad.licenciaprenatal
            #     #self.licencia_prenatal=self.licencia_maternidad.licenciaprenatal
            #     if diferencia_menos_de_5_meses(
            #         licencia_prenatal.fecha_inicio, self.fecha_inicio
            #     ):
            #         raise ValidationError(
            #             "Tiene que existir una distancia lógica entre ambas fechas"
            #         )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        fecha_de_inicio_del_embarazo = self.fecha_inicio
        if self.licencia_maternidad:
            licencia_prenatal=self.licencia_maternidad.licenciaprenatal
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
        return response

    def delete(self, *args, **kwargs):
        SegundaLicenciaPosnatal.objects.filter(licencia_maternidad=self.licencia_maternidad).delete()
        PrestacionSocial.objects.filter(licencia_maternidad=self.licencia_maternidad).delete()
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

    # primera_licencia_posnatal = models.OneToOneField(
    #     PrimeraLicenciaPosnatal,
    #     on_delete=models.CASCADE,
    #     verbose_name="Primera Licencia Posnatal",
    #
    # )
    prestacion_economica =models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Prestación Económica",
        validators=[MinValueValidator(0)],

    )
    licencia_maternidad = models.OneToOneField(
        LicenciaMaternidad,
        on_delete=models.CASCADE,
    )

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        if self.licencia_maternidad:
            licencia_prenatal=self.licencia_maternidad.licenciaprenatal
            if licencia_prenatal:
                self.prestacion_economica = (
                    licencia_prenatal.prestacion_economica
                )
        response = super().save(*args, **kwargs)

        crear_PrestacionSocial(
            self,
            PrestacionSocial.objects.filter(licencia_maternidad=self.licencia_maternidad).first()
            if not es_nuevo
            else None,
        )
        return response
    def __str__(self):
        return f"{self.licencia_maternidad.trabajador.nombre}"


def crear_SegundaLicenciaPosnatal(primera: PrimeraLicenciaPosnatal, segunda=None):
    if not segunda:
        segunda = SegundaLicenciaPosnatal()
    segunda.fecha_inicio = siguiente_dia_laborable(primera.fecha_fin)
    licencia_maternidad = primera.licencia_maternidad
    if licencia_maternidad:
        segunda.licencia_maternidad=licencia_maternidad
        licencia_prenatal=licencia_maternidad.licenciaprenatal
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

    # segunda_licencia_posnatal = models.OneToOneField(
    #     SegundaLicenciaPosnatal,
    #     on_delete=models.CASCADE,
    #     verbose_name="Segunda Licencia Posnatal",
    #
    # )
    prestacion_economica = models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Prestación Económica",
        validators=[MinValueValidator(0)],

    )
    licencia_maternidad = models.OneToOneField(
        LicenciaMaternidad,
        on_delete=models.CASCADE,
    )

    def clean(self):
        super().clean()
        if self.fecha_fin and self.fecha_inicio:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError(
                    "La fecha de inicio debe ser inferior a la fecha de fin "
                )

    def save(self, *args, **kwargs):
        cantidad_de_dias = dias_restantes_mes(self.fecha_inicio)
        if self.licencia_maternidad:
            licencia_prenatal=self.licencia_maternidad.licenciaprenatal
            if licencia_prenatal:
                SA = licencia_prenatal.salario_anual
                PM = (SA / 12) * 60 / 100
                self.prestacion_economica = 12 * PM
                if not cantidad_de_dias > 24:
                    PD = (PM / 24) * 60 / 100
                    self.prestacion_economica += cantidad_de_dias * PD
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.licencia_maternidad.trabajador.nombre}"


def crear_PrestacionSocial(segunda: SegundaLicenciaPosnatal, prestacion=None):
    if not prestacion:
        prestacion = PrestacionSocial()
    prestacion.fecha_inicio = siguiente_dia_laborable(segunda.fecha_fin)
    licencia_maternidad=segunda.licencia_maternidad
    if licencia_maternidad:
        primera_licencia_posnatal=licencia_maternidad.primeralicenciaposnatal
        if primera_licencia_posnatal:
            prestacion.fecha_fin = primer_cumpleannos(
                primera_licencia_posnatal.fecha_inicio
            )
        prestacion.licencia_maternidad=licencia_maternidad
    prestacion.save()


class PagoPorUtilidades(models.Model):
    fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    pago = models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Pago Por Utilidades", validators=[MinValueValidator(0)]
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )


class PagoPorSubsidios(models.Model):
    fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    pago = models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Pago Por Subsidios", validators=[MinValueValidator(0)]
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )


class SalarioMensualTotalPagado(models.Model):
    class Meta:
        verbose_name = "Salario Mensual"
        verbose_name_plural = "Salarios Mensuales"
    EVALUACIONES=[
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
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )
    salario_devengado_mensual = models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Salario Devengado Mensual",
        validators=[MinValueValidator(0)]
    )
    salario_basico_mensual = models.DecimalField(decimal_places=2, max_digits=15,
        verbose_name="Salario Basico Mensual", validators=[MinValueValidator(0)]
    )
    evaluacion_obtenida_por_el_jefe=models.CharField(
        verbose_name="Evaluación",
        max_length=256,
        choices=EVALUACIONES,
    )
    pago_por_utilidades = models.ForeignKey(
        PagoPorUtilidades,
        on_delete=models.SET_NULL,
        verbose_name="Pago Por Utilidades",
        null=True,
        blank=True,
    )

    pago_por_subsidios = models.ForeignKey(
        PagoPorSubsidios,
        on_delete=models.SET_NULL,
        verbose_name="Pago Por Subsidios",
        null=True,
        blank=True,
    )

    evaluacion_obtenida_por_el_jefe_en_puntos = models.IntegerField(
        verbose_name="Puntos", validators=[MinValueValidator(0)]
    )
    def get_evalucacion_str(self):
        for evaluacion in self.EVALUACIONES:
            if self.evaluacion_obtenida_por_el_jefe ==evaluacion[0]:
                return evaluacion[1]
        return ""
    def clean(self):
        super().clean()
        evaluacion = self.evaluacion_obtenida_por_el_jefe
        puntos=self.evaluacion_obtenida_por_el_jefe_en_puntos
        mensaje="Los puntos no son correctos"
        if evaluacion == "D":
            if puntos>60:
                raise ValidationError(
                    mensaje
                )
        elif evaluacion == "R":
            if puntos < 60 or puntos >79:
                raise ValidationError(
                    mensaje
                )
        elif evaluacion == "B":
            if puntos < 80 or puntos > 89:
                raise ValidationError(
                    mensaje
                )
        elif evaluacion == "MB":
            if puntos < 90 or puntos > 96:
                raise ValidationError(
                    mensaje
                )
        elif evaluacion == "E":
            if puntos < 97:
                raise ValidationError(
                    mensaje
                )

    def calcular_cantidad_de_horas_trabajadas_este_mes(self):
        asistencias=Asistencia.objects.filter(
            fecha__year=self.fecha.year,
            fecha__month=self.fecha.month
        )

        suma=0
        for asistencia in asistencias:
            suma+=asistencia.horas_trabajadas
        # print(suma)
        dias_feriados=get_dias_feriado(self.fecha.month)
        if dias_feriados:
            SDSA = calcular_SDSA(self.fecha, self.trabajador)
            for dia in dias_feriados:
                viernes=es_viernes(self.fecha.replace(day=dia))
                # print(f"SDSA {SDSA}")
                suma +=len(dias_feriados)*(9 if not viernes else 8)*SDSA
        return suma
    def actualizar_salario(self):
        evaluacion=self.evaluacion_obtenida_por_el_jefe#self.trabajador.salario_escala
        salario_escala=self.trabajador.salario_escala
        if evaluacion == "D":
            salario_basico_seleccionado=salario_escala.rango_salarial_1
        elif evaluacion == "R":
            salario_basico_seleccionado=salario_escala.rango_salarial_2
        elif evaluacion == "B":
            salario_basico_seleccionado=salario_escala.rango_salarial_3
        elif evaluacion == "MB":
            salario_basico_seleccionado=salario_escala.rango_salarial_4
        elif evaluacion == "E":
            salario_basico_seleccionado=salario_escala.rango_salarial_5
        else:
            salario_basico_seleccionado=0

        self.salario_basico_mensual=salario_basico_seleccionado

        self.salario_devengado_mensual = salario_basico_seleccionado
        self.salario_devengado_mensual*= self.evaluacion_obtenida_por_el_jefe_en_puntos / 100
        self.salario_devengado_mensual /=  190.6
        self.salario_devengado_mensual*=self.calcular_cantidad_de_horas_trabajadas_este_mes()
        if self.pago_por_utilidades:
            self.salario_devengado_mensual -= self.pago_por_utilidades.pago
        if self.pago_por_subsidios:
            self.salario_devengado_mensual -= self.pago_por_subsidios.pago


    def save(self, *args, **kwargs):
        self.actualizar_salario()
        return super().save(*args, **kwargs)

    # @staticmethod
    # def calcular_pago_maternidad(year_actual,trabajador):
    #     SA=SalarioMensualTotalPagado.calcular_salario_anual(year_actual-1,trabajador)

    def __str__(self):
        return f"{self.trabajador.nombre} {self.trabajador.apellidos} {self.fecha}"

def calcular_promedio_salario(fecha, trabajador, cantidad_de_meses):
    fecha_limite_inferior = fecha - timezone.timedelta(days=365)
    fecha_limite_inferior.replace(day=1)
    SA = (
        SalarioMensualTotalPagado.objects.filter(
            fecha__gte=fecha_limite_inferior, trabajador=trabajador
        )
        .order_by("-fecha")[:cantidad_de_meses]
        .aggregate(total=Sum("salario_devengado_mensual"))["total"]
    )
    return SA if SA else 0
def calcular_SA(fecha, trabajador):
    return calcular_promedio_salario(fecha, trabajador, 12)

def calcular_SDSA(fecha, trabajador):
    return calcular_promedio_salario(fecha, trabajador, 6)

# class Cargo(models.Model):
#     class Meta:
#         verbose_name = "Cargo"
#         verbose_name_plural = "Cargos"
#
#     cargo = models.CharField(
#         verbose_name="Cargo", max_length=256, validators=[not_empty_validation]
#     )
#     salario_basico = models.FloatField(
#         verbose_name="Salario Basico", validators=[MinValueValidator(0)]
#     )
#
#     def __str__(self):
#         return self.cargo


# class Escala(models.Model):
#     class Meta:
#         verbose_name = "Escala"
#         verbose_name_plural = "Escalas"
#
#     escala = models.CharField(
#         verbose_name="Escala", max_length=256, validators=[not_empty_validation]
#     )
#     salario_basico = models.FloatField(
#         verbose_name="Salario Basico", validators=[MinValueValidator(0)]
#     )
#
#     def __str__(self):
#         return self.escala
