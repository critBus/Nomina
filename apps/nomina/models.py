from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
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


class Cargo(models.Model):
    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    cargo = models.CharField(
        verbose_name="Cargo", max_length=256, validators=[not_empty_validation]
    )
    salario_basico = models.FloatField(
        verbose_name="Salario Basico", validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.cargo


class Escala(models.Model):
    class Meta:
        verbose_name = "Escala"
        verbose_name_plural = "Escalas"

    escala = models.CharField(
        verbose_name="Escala", max_length=256, validators=[not_empty_validation]
    )
    salario_basico = models.FloatField(
        verbose_name="Salario Basico", validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.escala


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
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE, verbose_name="Escala")
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name="Cargo")

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
