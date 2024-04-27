from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone


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
        verbose_name="Cargo", max_length=256,choices=[("I","I",),("II","II",)]
    )
    grupo_escala = models.CharField(
        verbose_name="Cargo", max_length=256, choices=[("II","II",),
                                                        ("III", "III",),
                                                       ("IV", "IV",),
                                                       ("V", "V",),
                                                       ("IV", "IV",)
                                                       ]
    )
    rango_salarial=models.IntegerField(choices=(
        (1, 'Rango Salarial 1'),
        (2, 'Rango Salarial 2'),
        (3, 'Rango Salarial 3'),
        (4, 'Rango Salarial 4'),
        (5, 'Rango Salarial 5'),
    ))

    salario = models.FloatField(
        verbose_name="Salario", validators=[MinValueValidator(0)]
    )

    @property
    def categoria_ocupacional(self):
        return "Operario" if (self.grupo_complejidad == "I") else "Servicios"

    def __str__(self):
        return f"{self.grupo_complejidad} {self.grupo_escala} {self.rango_salarial} {self.salario}"


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
    salario_escala = models.ForeignKey(SalarioEscala,
                                       on_delete=models.SET_NULL,
                                       verbose_name="Salario Escala",null=True,blank=True)
    # escala = models.ForeignKey(Escala, on_delete=models.CASCADE, verbose_name="Escala")
    # cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name="Cargo")

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
        default=8,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )

    def __str__(self):
        return f"{self.trabajador.nombre} {self.trabajador.apellidos} {self.fecha}"


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


class CertificadoMaternidad(models.Model):
    class Meta:
        unique_together = (
            (
                "trabajador",
                "fecha_inicio",
            ),
        )
        verbose_name = "Certificado Maternidad"
        verbose_name_plural = "Certificados de Maternidad"

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

class PagoPorUtilidades(models.Model):
    fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    pago = models.FloatField(
        verbose_name="Pago Por Utilidades",
        validators=[MinValueValidator(0)]
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )

class PagoPorSubsidios(models.Model):
    fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    pago = models.FloatField(
        verbose_name="Pago Por Subsidios",
        validators=[MinValueValidator(0)]
    )
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )
class SalarioMensualTotalPagado(models.Model):
    fecha = models.DateField(verbose_name="Fecha",default=timezone.now)
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, verbose_name="Trabajador"
    )
    salario_devengado_mensual=models.FloatField(
        verbose_name="Salario Devengado Mensual",
        validators=[MinValueValidator(0)]
    )
    salario_basico_mensual = models.FloatField(
        verbose_name="Salario Basico Mensual",
        validators=[MinValueValidator(0)]
    )
    pago_por_utilidades = models.ForeignKey(
        PagoPorUtilidades,
        on_delete=models.SET_NULL,
        verbose_name="Pago Por Utilidades",
        null=True, blank=True
    )

    pago_por_subsidios=models.ForeignKey(
        PagoPorSubsidios,
        on_delete=models.SET_NULL,
        verbose_name="Pago Por Subsidios",
        null=True,blank=True
    )

    def actualizar_salario_devengado(self):
        self.salario_devengado_mensual=self.salario_basico_mensual
        if self.pago_por_utilidades:
            self.salario_devengado_mensual-=self.pago_por_utilidades.pago
        if self.pago_por_subsidios:
            self.salario_devengado_mensual-=self.pago_por_subsidios.pago
    # @staticmethod
    # def calcular_salario_anual(year,trabajador):
    #     #SA
    #     return SalarioMensualTotalPagado.objects.filter(
    #         fecha__year=year,trabajador=trabajador
    #     ).aggregate(total=Sum('salario_basico_mensual'))['total']
    #
    # @staticmethod
    # def calcular_importe_semanal(year,trabajador):
    #     #ISP
    #     SA=SalarioMensualTotalPagado.calcular_salario_anual(year,trabajador)
    #     return SA/52

    def calcular_pago_licencia_maternidad_base(self,fecha,trabajador,es_simple:bool):
        fecha_limite_inferior=fecha-timezone.timedelta(days=365)
        fecha_limite_inferior.replace(day=1)
        SA = SalarioMensualTotalPagado.objects.filter(
            fecha__gte=fecha_limite_inferior,trabajador=trabajador
        ).order_by("-fecha")[:12].aggregate(total=Sum('salario_basico_mensual'))['total']
        ISP=SA/52
        Pres_Eco=ISP * 6 if es_simple else ISP * 8
        return Pres_Eco

    def calcular_pago_licencia_prenatal(self,fecha_de_inicio_del_embarazo ,trabajador,es_simple:bool):
        Pres_Eco =self.calcular_pago_licencia_maternidad_base(fecha_de_inicio_del_embarazo,trabajador,es_simple)
        return Pres_Eco

    def calcular_pago_licencia_posnatal(self,fecha_de_inicio_del_embarazo ,trabajador,es_simple:bool):
        Pres_Eco =self.calcular_pago_licencia_maternidad_base(fecha_de_inicio_del_embarazo,trabajador,es_simple)
        return Pres_Eco

    def save(self, *args, **kwargs):
        self.actualizar_salario_devengado()
        return super().save(*args, **kwargs)

    # @staticmethod
    # def calcular_pago_maternidad(year_actual,trabajador):
    #     SA=SalarioMensualTotalPagado.calcular_salario_anual(year_actual-1,trabajador)





    def __str__(self):
        return f"{self.trabajador.nombre} {self.trabajador.apellidos} {self.fecha}"





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