from django.contrib import admin
from .models import *
from apps.users.models import User
# Register your models here.

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = (
        "cargo",
        "salario_basico",

    )
    search_fields = (
        "cargo",
        "salario_basico",
    )
    list_filter = ("cargo",)
    ordering = (
        "cargo",
        "salario_basico",
    )

@admin.register(Escala)
class EscalaAdmin(admin.ModelAdmin):
    list_display = (
        "escala",
        "salario_basico",
    )
    search_fields = (
        "escala",
        "salario_basico",
    )
    list_filter = ("escala",)
    ordering = (
        "escala",
        "salario_basico",
    )


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = (
        "carnet",
        "nombre",
        "apellidos",
        "categoria_ocupacional",
        "email",
        "telefono",
    )
    search_fields = (
        "carnet",
        "nombre",
        "apellidos",
        "categoria_ocupacional",
        "email",
        "telefono",
    )
    list_filter = ("escala",)
    ordering = (
        "carnet",
        "nombre",
        "apellidos",
        "categoria_ocupacional",
        "email",
        "telefono",
    )


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "horas_trabajadas",
        "trabajador"
    )
    search_fields = (
        "fecha",
        "horas_trabajadas",
        "trabajador",
    )
    list_filter = ("horas_trabajadas","trabajador",)
    ordering = (
        "fecha",
        "horas_trabajadas",
        "trabajador",
    )
    date_hierarchy = "fecha"


@admin.register(CertificadoMedico)
class CertificadoMedicoAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador"
    )
    search_fields = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    list_filter = ("fecha_inicio",
        "fecha_fin","trabajador",)
    ordering = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    date_hierarchy = "fecha_inicio"



@admin.register(CertificadoMaternidad)
class CertificadoMaternidadAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador"
    )
    search_fields = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    list_filter = ("fecha_inicio",
        "fecha_fin","trabajador",)
    ordering = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    date_hierarchy = "fecha_inicio"