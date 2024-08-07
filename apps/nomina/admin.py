from django.contrib import admin
from django.db.models import BooleanField, Case, CharField, Q, Value, When

from apps.users.models import User
from config.utils.utils_reportes import AdministradorDeReporte

from .models import *
from .utils.utils_reportes_d import (
    general_reporte_prestacion_social_pdf,
    generar_reporte_certificados,
    generar_reporte_historial_de_evaluacion_pdf,
    generar_reporte_maternidad_pdf,
    generar_reporte_salario_en_el_anno_pdf,
    generar_reporte_sbm,
    generar_reporte_sdm,
    generar_reporte_utilidades_pdf,
)


class LicenciaPrenatalInline(admin.StackedInline):
    model = LicenciaPrenatal
    extra = 1  # Número de campos extra en el formulario
    readonly_fields = (
        "fecha_fin",
        "prestacion_economica",
        "importe_semanal",
        "salario_anual",
    )
    min_num = 1
    max_num = 1
    exclude = [
        "trabajador",
        "pago_mensual",
        "date_range",
    ]
    can_delete = False


class PrimeraLicenciaPosnatalInline(admin.StackedInline):
    model = PrimeraLicenciaPosnatal
    extra = 1  # Número de campos extra en el formulario
    readonly_fields = ("prestacion_economica",)
    exclude = [
        "pago_mensual",
        "date_range",
    ]
    max_num = 1


class SegundaLicenciaPosnatalInline(admin.StackedInline):
    model = SegundaLicenciaPosnatal
    extra = 1  # Número de campos extra en el formulario
    readonly_fields = (
        "fecha_inicio",
        "fecha_fin",
        "prestacion_economica",
    )
    exclude = [
        "pago_mensual",
        "date_range",
    ]
    # min_num = 1
    max_num = 1
    can_delete = False


class PrestacionSocialInline(admin.StackedInline):
    model = PrestacionSocial
    extra = 1  # Número de campos extra en el formulario
    readonly_fields = (
        "fecha_inicio",
        "fecha_fin",
        "prestacion_economica",
    )
    exclude = [
        "pago_mensual",
        "date_range",
    ]
    can_delete = False
    # min_num = 1
    max_num = 1


class primera_licencia_posnatal_Filter(admin.SimpleListFilter):
    title = "Primera Posnatal"
    parameter_name = "nada"

    def lookups(self, request, model_admin):
        return ((True, True), (False, False))

    def queryset(self, request, queryset):
        # apply the filter to the queryset
        if self.value():
            valor = self.value()
            # print(valor)
            # print(type(valor))
            return queryset.filter(
                primeralicenciaposnatal__isnull=valor.lower() == "false"
            )
        return queryset


@admin.register(LicenciaMaternidad)
class LicenciaMaternidadAdmin(admin.ModelAdmin):
    # readonly_fields = ("fecha_inicio",)
    exclude = [
        "fecha_inicio",
    ]
    inlines = [
        LicenciaPrenatalInline,
        PrimeraLicenciaPosnatalInline,
        SegundaLicenciaPosnatalInline,
        PrestacionSocialInline,
    ]
    list_display = (
        "trabajador",
        "fecha_inicio",
        "view_primera_licencia_posnatal",
    )
    search_fields = (
        "trabajador__nombre",
        "fecha_inicio",
    )
    list_filter = ("trabajador", "fecha_inicio", primera_licencia_posnatal_Filter)
    ordering = (
        "trabajador",
        "fecha_inicio",
    )
    date_hierarchy = "fecha_inicio"

    actions = [generar_reporte_maternidad_pdf, general_reporte_prestacion_social_pdf]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "trabajador":
            kwargs["queryset"] = Trabajador.objects.filter(sexo="Femenino")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                hay_primera_licencia_posnatal=Case(
                    When(
                        primeralicenciaposnatal__isnull=True,
                        then=False,
                    ),
                    default=True,
                    output_field=BooleanField(),
                )
            )
        )

    def view_primera_licencia_posnatal(self, obj):
        return PrimeraLicenciaPosnatal.objects.filter(licencia_maternidad=obj).exists()

    view_primera_licencia_posnatal.admin_order_field = "hay_primera_licencia_posnatal"
    view_primera_licencia_posnatal.short_description = "Primera Licencia Posnatal"

    def before_save(self, request, obj, form, change):
        prenatal = obj.licenciaprenatal
        if prenatal:
            prenatal.trabajador = obj.trabajador
            obj.fecha_inicio = prenatal.fecha_inicio

    def save_related(self, request, form, formsets, change):
        # Llama a la función antes de guardar los modelos
        self.before_save(request, form.instance, form, change)

        super().save_related(request, form, formsets, change)

    def save_model(self, request, obj, form, change):
        # Llama a la función antes de guardar los modelos
        self.before_save(request, form.instance, form, change)
        response = super().save_model(request, obj, form, change)
        return response


class categoria_ocupacional_Filter(admin.SimpleListFilter):
    title = "Categoria Ocupacional"
    parameter_name = "nada"

    def lookups(self, request, model_admin):
        return (
            ("Operario", "Operario"),
            ("Servicios", "Servicios"),
            ("Técnicos de actividad o gestion", "Técnicos de actividad o gestion"),
            (
                "Técnicos gestores de actividad de gestion",
                "Técnicos gestores de actividad de gestion",
            ),
            ("Técnicos actividades generales", "Técnicos actividades generales"),
            (
                "Técnicos gestores actividades principales",
                "Técnicos gestores actividades principales",
            ),
        )

    def queryset(self, request, queryset):
        # apply the filter to the queryset
        if self.value():
            valor = self.value()
            grupo_complejidad = "VI"
            if valor == "Operario":
                grupo_complejidad = "I"

            elif valor == "Servicios":
                grupo_complejidad = "II"

            elif valor == "Técnicos de actividad o gestion":
                grupo_complejidad = "III"

            elif valor == "Técnicos gestores de actividad de gestion":
                grupo_complejidad = "IV"

            elif valor == "Técnicos actividades generales":
                grupo_complejidad = "V"

            return queryset.filter(grupo_complejidad=grupo_complejidad)

        return queryset


@admin.register(SalarioEscala)
class SalarioEscalaAdmin(admin.ModelAdmin):
    list_display = (
        "grupo_complejidad",
        "grupo_escala",
        # "rango_salarial",
        # "salario",
        "view_categoria_ocupacional",
        "rango_salarial_1",
        "rango_salarial_2",
        "rango_salarial_3",
        "rango_salarial_4",
        "rango_salarial_5",
        # "categoria_ocupacional",
    )
    search_fields = (
        "grupo_complejidad",
        "grupo_escala",
        # "rango_salarial",
        # "salario",
        "rango_salarial_1",
        "rango_salarial_2",
        "rango_salarial_3",
        "rango_salarial_4",
        "rango_salarial_5",
        # "categoria_ocupacional",
    )
    list_filter = (
        "grupo_complejidad",
        "grupo_escala",
        # "rango_salarial",
        categoria_ocupacional_Filter,
    )
    ordering = (
        "grupo_complejidad",
        "grupo_escala",
        # "rango_salarial",
        # "salario",
        "rango_salarial_1",
        "rango_salarial_2",
        "rango_salarial_3",
        "rango_salarial_4",
        "rango_salarial_5",
        # "categoria_ocupacional",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                categoria_ocupacional2=Case(
                    When(
                        grupo_complejidad="I",
                        then=Value("Operario"),
                    ),
                    When(
                        grupo_complejidad="II",
                        then=Value("Servicios"),
                    ),
                    When(
                        grupo_complejidad="III",
                        then=Value("Técnicos de actividad o gestion"),
                    ),
                    When(
                        grupo_complejidad="IV",
                        then=Value("Técnicos gestores de actividad de gestion"),
                    ),
                    When(
                        grupo_complejidad="V",
                        then=Value("Técnicos actividades generales"),
                    ),
                    When(
                        grupo_complejidad="IV",
                        then=Value("Técnicos gestores actividades principales"),
                    ),
                    default=Value("Técnicos gestores actividades principales"),
                    output_field=CharField(),
                )
            )
        )

    def view_categoria_ocupacional(self, obj):
        return obj.categoria_ocupacional

    view_categoria_ocupacional.admin_order_field = "categoria_ocupacional2"
    view_categoria_ocupacional.short_description = "Categoria Ocupacional"


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = (
        "carnet",
        "nombre",
        "apellidos",
        "cargo",
        "email",
        "telefono",
    )
    search_fields = (
        "carnet",
        "nombre",
        "apellidos",
        "cargo",
        "email",
        "telefono",
    )
    list_filter = ("cargo",)
    ordering = (
        "carnet",
        "nombre",
        "apellidos",
        "cargo",
        "email",
        "telefono",
    )
    # actions = [generar_pdf]


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "horas_trabajadas", "trabajador")
    search_fields = (
        "fecha",
        "horas_trabajadas",
        "trabajador__nombre",
    )
    list_filter = (
        "horas_trabajadas",
        "trabajador",
        "fecha",
    )
    ordering = (
        "fecha",
        "horas_trabajadas",
        "trabajador",
    )
    date_hierarchy = "fecha"


class PrimerCertificadoMedicoInline(admin.StackedInline):
    model = PrimerCertificadoMedico
    extra = 1
    readonly_fields = (
        "prestacion_economica",
        "horas_laborales",
        "horas_laborales_en_dias_de_carencia",
    )
    min_num = 1
    can_delete = False
    exclude = [
        "pago_mensual",
        "date_range",
    ]


class ExtraCertificadoMedicoInline(admin.StackedInline):
    model = ExtraCertificadoMedico
    extra = 1
    readonly_fields = (
        "prestacion_economica",
        "horas_laborales",
        "horas_laborales_en_dias_de_carencia",
    )

    exclude = [
        "pago_mensual",
        "date_range",
    ]


@admin.register(CertificadoMedicoGeneral)
class CertificadoMedicoGeneralAdmin(admin.ModelAdmin):
    inlines = [PrimerCertificadoMedicoInline, ExtraCertificadoMedicoInline]
    readonly_fields = (
        "salario_anual",
        "fecha_inicio",
    )
    list_display = (
        "fecha_inicio",
        "trabajador",
        "ingresado",
    )
    search_fields = (
        "fecha_inicio",
        "ingresado",
        "trabajador__nombre",
    )
    list_filter = (
        "fecha_inicio",
        "ingresado",
        "trabajador",
    )
    ordering = (
        "fecha_inicio",
        "ingresado",
        "trabajador",
    )
    date_hierarchy = "fecha_inicio"


@admin.register(SalarioMensualTotalPagado)
class SalarioMensualTotalPagadoAdmin(admin.ModelAdmin):
    readonly_fields = (
        "salario_devengado_mensual",
        "salario_basico_mensual",
        "evaluacion_obtenida_por_el_jefe",
        "horas_trabajadas",
        "pago_por_dias_feriados",
        "pago_certificados_medicos",
        "pago_certificados_maternidad",
        "pago_utilidades",
        "pago_total",
        "salario_anual",
        "salario_devengado_semi_anual",
    )
    list_display = (
        "fecha",
        "trabajador",
        "pago_total",
        "salario_devengado_mensual",
        "evaluacion_obtenida_por_el_jefe",
    )
    search_fields = (
        "fecha",
        "trabajador__nombre",
        "pago_total",
        "salario_devengado_mensual",
        "evaluacion_obtenida_por_el_jefe",
    )
    list_filter = (
        "fecha",
        "trabajador",
        "evaluacion_obtenida_por_el_jefe",
    )
    ordering = (
        "fecha",
        "trabajador",
        "salario_devengado_mensual",
        "evaluacion_obtenida_por_el_jefe",
        "pago_total",
    )
    date_hierarchy = "fecha"
    actions = [
        generar_reporte_sdm,
        generar_reporte_sbm,
        generar_reporte_certificados,
        generar_reporte_historial_de_evaluacion_pdf,
        generar_reporte_salario_en_el_anno_pdf,
    ]


@admin.register(PagoPorUtilidadesAnuales)
class PagoPorUtilidadesAnualesAdmin(admin.ModelAdmin):
    readonly_fields = (
        "salario_anual",
        "tiempo_real_trabajado_en_dias",
        "pago",
    )
    list_display = (
        "fecha",
        "trabajador",
        "pago",
        "pago_extra",
    )
    search_fields = (
        "fecha",
        "trabajador__nombre",
    )
    list_filter = (
        "fecha",
        "trabajador",
    )
    ordering = (
        "fecha",
        "trabajador",
    )
    date_hierarchy = "fecha"
    actions = [generar_reporte_utilidades_pdf]
    exclude = [
        "pago_mensual",
    ]


@admin.register(PlanificacionUtilidadesAnuales)
class PlanificacionUtilidadesAnualesAdmin(admin.ModelAdmin):
    readonly_fields = (
        "sobrante",
        "sobrante_por_trabajador",
    )
    list_display = (
        "fecha",
        "year",
        "dinero_a_repartir",
        "sobrante",
        "sobrante_por_trabajador",
    )
    search_fields = (
        "fecha",
        "year",
        "dinero_a_repartir",
        "sobrante",
        "sobrante_por_trabajador",
    )
    list_filter = (
        "fecha",
        "year",
    )
    ordering = (
        "fecha",
        "year",
        "dinero_a_repartir",
        "sobrante",
        "sobrante_por_trabajador",
    )
    date_hierarchy = "fecha"


@admin.register(DiaFeriado)
class DiaFeriadoAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "nombre",
    )
    search_fields = (
        "fecha",
        "nombre",
    )
    list_filter = (
        "nombre",
        "fecha",
    )
    ordering = (
        "fecha",
        "nombre",
    )
    date_hierarchy = "fecha"
