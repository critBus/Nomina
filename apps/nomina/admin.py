from django.contrib import admin

from apps.users.models import User
from config.utils.utils_reportes import AdministradorDeReporte

from .models import *
from django_reportbroD.reportcore import reportPDF

@admin.register(SalarioEscala)
class SalarioEscalaAdmin(admin.ModelAdmin):
    pass

def generar_pdf(modeladmin, request, queryset):

    trabajadores = queryset


    data = {"trabajadores": [{
        "nombre":v.nombre,
        "apellidos":v.apellidos,
        "cargo": v.cargo.cargo
    } for v in trabajadores],}

    code_report = 1

    return reportPDF(request, code_report, data, file="reporte trabajadores")


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = (
        "carnet",
        "nombre",
        "apellidos",
        # "categoria_ocupacional",
        "email",
        "telefono",
    )
    search_fields = (
        "carnet",
        "nombre",
        "apellidos",
        # "categoria_ocupacional",
        "email",
        "telefono",
    )
    # list_filter = ("escala",)
    ordering = (
        "carnet",
        "nombre",
        "apellidos",
        # "categoria_ocupacional",
        "email",
        "telefono",
    )
    actions = [generar_pdf]



@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "horas_trabajadas", "trabajador")
    search_fields = (
        "fecha",
        "horas_trabajadas",
        "trabajador",
    )
    list_filter = (
        "horas_trabajadas",
        "trabajador",
    )
    ordering = (
        "fecha",
        "horas_trabajadas",
        "trabajador",
    )
    date_hierarchy = "fecha"


@admin.register(CertificadoMedico)
class CertificadoMedicoAdmin(admin.ModelAdmin):
    list_display = ("fecha_inicio", "fecha_fin", "trabajador")
    search_fields = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    list_filter = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    ordering = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    date_hierarchy = "fecha_inicio"


@admin.register(CertificadoMaternidad)
class CertificadoMaternidadAdmin(admin.ModelAdmin):
    list_display = ("fecha_inicio", "fecha_fin", "trabajador")
    search_fields = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    list_filter = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    ordering = (
        "fecha_inicio",
        "fecha_fin",
        "trabajador",
    )
    date_hierarchy = "fecha_inicio"



# Register your models here.
#
# REPORTE_Cargo_PDF=AdministradorDeReporte()
# REPORTE_Cargo_PDF.setClaseModelo(Cargo)
# REPORTE_Cargo_PDF.titulo="Cargos"
# REPORTE_Cargo_PDF.add('Cargo',lambda v:v.cargo)
# REPORTE_Cargo_PDF.add('Salario Basico',lambda v:v.salario_basico)
# REPORTE_Cargo_PDF.add('Trabajadores',lambda v:"<br/>".join([f"{z.nombre} {z.apellidos}" for z in v.trabajador_set.all()]))
#
#
#
# @admin.register(Cargo)
# class CargoAdmin(admin.ModelAdmin):
#     list_display = (
#         "cargo",
#         "salario_basico",
#     )
#     search_fields = (
#         "cargo",
#         "salario_basico",
#     )
#     list_filter = ("cargo",)
#     ordering = (
#         "cargo",
#         "salario_basico",
#     )
#     actions = [REPORTE_Cargo_PDF.getAction()]
#
# REPORTE_Escala_PDF=AdministradorDeReporte()
# REPORTE_Escala_PDF.setClaseModelo(Cargo)
# REPORTE_Escala_PDF.titulo="Escala"
# REPORTE_Escala_PDF.add('Escala',lambda v:v.escala)
# REPORTE_Escala_PDF.add('Salario Basico',lambda v:v.salario_basico)
# REPORTE_Escala_PDF.add('Trabajadores',lambda v:"<br/>".join([f"{z.nombre} {z.apellidos}" for z in v.trabajador_set.all()]))
#
# @admin.register(Escala)
# class EscalaAdmin(admin.ModelAdmin):
#     list_display = (
#         "escala",
#         "salario_basico",
#     )
#     search_fields = (
#         "escala",
#         "salario_basico",
#     )
#     list_filter = ("escala",)
#     ordering = (
#         "escala",
#         "salario_basico",
#     )
