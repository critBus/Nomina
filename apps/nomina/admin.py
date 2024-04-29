from django.contrib import admin
from django_reportbroD.reportcore import reportPDF

from apps.users.models import User
from config.utils.utils_reportes import AdministradorDeReporte

from .models import *


class LicenciaPrenatalInline(admin.StackedInline):
    model = LicenciaPrenatal
    extra = 1  # Número de campos extra en el formulario
    readonly_fields = (

        "prestacion_economica",
        "importe_semanal",
        "salario_anual",
    )
    min_num = 1
    max_num = 1
    exclude = ["trabajador",]
    can_delete = False
#
# from django.forms.models import BaseInlineFormSet
# class ItemInlineFormSet(BaseInlineFormSet):
#    def clean(self):
#       super(ItemInlineFormSet, self).clean()

class PrimeraLicenciaPosnatalInline(admin.StackedInline):
    model = PrimeraLicenciaPosnatal
    extra = 1  # Número de campos extra en el formulario
    readonly_fields = (

        "prestacion_economica",
    )
    #min_num = 1
    max_num = 1
    # exclude = ["licencia_prenatal",]
    # formset = ItemInlineFormSet


class SegundaLicenciaPosnatalInline(admin.StackedInline):
    model = SegundaLicenciaPosnatal
    extra = 1  # Número de campos extra en el formulario
    readonly_fields = (
        "fecha_inicio",
        "fecha_fin",
        "prestacion_economica",
    )
    #min_num = 1
    max_num = 1
    can_delete = False
    # exclude = ["primera_licencia_posnatal",]


class PrestacionSocialInline(admin.StackedInline):
    model = PrestacionSocial
    extra = 1  # Número de campos extra en el formulario
    readonly_fields = (
        "fecha_inicio",
        "fecha_fin",
        "prestacion_economica",
    )
    can_delete=False
    #min_num = 1
    max_num = 1
    # exclude = ["segunda_licencia_posnatal",]


    # def clean(self):
    #     super().clean()
    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj, **kwargs)
    #     # Realiza la modificación del valor aquí
    #     #formset.form.base_fields['campo_a_modificar'].initial = 'Nuevo-Valor'
    #     return formset

@admin.register(LicenciaMaternidad)
class LicenciaMaternidadAdmin(admin.ModelAdmin):
    #readonly_fields = ("fecha_inicio",)
    exclude = ["fecha_inicio", ]
    inlines = [
        LicenciaPrenatalInline,
        PrimeraLicenciaPosnatalInline,
        SegundaLicenciaPosnatalInline,
        PrestacionSocialInline,
    ]
    list_display = (
        "trabajador",
        "fecha_inicio",
    )
    search_fields = (
        "trabajador",
        "fecha_inicio",
    )
    list_filter = (
        "trabajador",
        "fecha_inicio",
    )
    ordering = (
        "trabajador",
        "fecha_inicio",
    )
    date_hierarchy = "fecha_inicio"

    def before_save(self, request, obj, form, change):
        prenatal = obj.licenciaprenatal
        if prenatal:
            prenatal.trabajador = obj.trabajador
            obj.fecha_inicio = prenatal.fecha_inicio
        # if hasattr(obj,"primeralicenciaposnatal"):
        #     primera=obj.primeralicenciaposnatal
        #     if primera:
        #         if not prenatal:
        #             pass
        #         primera.licencia_prenatal=prenatal


        # if obj.atributo_seleccionado == 'valor_especifico':
        # for inline_formset in self.get_inline_instances(request, obj):
        #     for form in inline_formset:
        #         if getattr(form, "Meta").model == LicenciaPrenatal:
        #             form.instance.trabajador = obj.trabajador
        #             obj.fecha_inicio = form.instance.fecha_inicio
        #             return

    def save_related(self, request, form, formsets, change):
        # Llama a la función antes de guardar los modelos
        self.before_save(request, form.instance, form, change)

        super().save_related(request, form, formsets, change)

    def save_model(self, request, obj, form, change):

        # Llama a la función antes de guardar los modelos
        self.before_save(request, form.instance, form, change)
        response = super().save_model(request, obj, form, change)
        return response


@admin.register(SalarioEscala)
class SalarioEscalaAdmin(admin.ModelAdmin):
    pass


def generar_pdf(modeladmin, request, queryset):
    trabajadores = queryset

    data = {
        "trabajadores": [
            {"nombre": v.nombre, "apellidos": v.apellidos, "cargo": v.cargo.cargo}
            for v in trabajadores
        ],
    }

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


# @admin.register(CertificadoMaternidad)
# class CertificadoMaternidadAdmin(admin.ModelAdmin):
#     list_display = ("fecha_inicio", "fecha_fin", "trabajador")
#     search_fields = (
#         "fecha_inicio",
#         "fecha_fin",
#         "trabajador",
#     )
#     list_filter = (
#         "fecha_inicio",
#         "fecha_fin",
#         "trabajador",
#     )
#     ordering = (
#         "fecha_inicio",
#         "fecha_fin",
#         "trabajador",
#     )
#     date_hierarchy = "fecha_inicio"


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
