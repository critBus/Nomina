import json
from typing import List

from django.shortcuts import redirect
from django.urls import reverse
from django_reportbroD.reportcore import reportPDF
from django_reportbroD.utils import export_report_by_name

from ..models import *
from .util_email_reporte_d import custom_export_report_by_name

# def redireccionar_a_vista_pdf(nombre_plantilla,data):
#     data_pdf = json.dumps(data)
#     url = reverse('generalpdf') + f"?nombre_template={nombre_plantilla}&data_pdf={data_pdf}"
#     return redirect(url)


def redireccionar_a_vista_pdf(nombre_url, queryset):
    data_pdf = json.dumps({"lista_ids": [v.id for v in queryset]})
    url = reverse(nombre_url) + f"?data_pdf={data_pdf}"
    return redirect(url)


# def generar_reporte_trabajadores_pdf(modeladmin, request, queryset):
#     trabajadores = queryset
#
#     data = {
#         "trabajadores": [
#             {"nombre": v.nombre, "apellidos": v.apellidos, "cargo": v.cargo.cargo}
#             for v in trabajadores
#         ],
#     }
#
#     code_report = 1
#
#     return reportPDF(request, code_report, data, file="reporte trabajadores")


def generar_reporte_maternidad_pdf(
    modeladmin, request, queryset
):  # generar_reporte_maternidad_pdf
    # return redireccionar_a_vista_pdf("generar_reporte_maternidad_view", queryset)

    entidades: List[LicenciaMaternidad] = queryset
    lista = []
    for licencia in entidades:
        data_licencia = {
            "nombre": licencia.trabajador.nombre,
            "apellidos": licencia.trabajador.apellidos,
            "ci": licencia.trabajador.carnet,
            "cargo": licencia.trabajador.cargo,
        }
        pre: LicenciaPrenatal = LicenciaPrenatal.objects.filter(
            licencia_maternidad=licencia
        ).first()
        data_licencia["Lic_Pre"] = float(pre.prestacion_economica) if pre else None
        pre: PrimeraLicenciaPosnatal = PrimeraLicenciaPosnatal.objects.filter(
            licencia_maternidad=licencia
        ).first()
        data_licencia["Lic_Pos_1"] = float(pre.prestacion_economica) if pre else None
        pre: SegundaLicenciaPosnatal = SegundaLicenciaPosnatal.objects.filter(
            licencia_maternidad=licencia
        ).first()
        data_licencia["Lic_Pos_2"] = float(pre.prestacion_economica) if pre else None
        lista.append(data_licencia)

    data = {"lista": lista, "nombre_reporte": "Control de la Prestación de Pago"}

    return custom_export_report_by_name(
        "Control de la Prestación de Pago", data, file="reporte", send_email=True
    )


def generar_reporte_sdm(modeladmin, request, queryset):
    # return redireccionar_a_vista_pdf("generar_reporte_sdm_view", queryset)
    entidades: List[SalarioMensualTotalPagado] = queryset.order_by("fecha")
    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.cargo,
            "ci": entidad.trabajador.carnet,
            "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
            "year": entidad.fecha.year,
            "mes": entidad.fecha.month,
            "Pago": float(entidad.salario_devengado_mensual),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "nombre_reporte": "Salario Devengado",
        "fecha_imprecion": timezone.now(),
    }
    return custom_export_report_by_name(
        "Salario Devengado", data, file="reporte", send_email=True
    )


def generar_reporte_sbm(modeladmin, request, queryset):
    # return redireccionar_a_vista_pdf("generar_reporte_sbm_view", queryset)
    entidades: List[SalarioMensualTotalPagado] = queryset.order_by("fecha")

    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.cargo,
            "ci": entidad.trabajador.carnet,
            "year": entidad.fecha.year,
            "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
            "mes": entidad.fecha.month,
            "Pago": float(entidad.pago_total),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "nombre_reporte": "Pre-nomina",
        "fecha_imprecion": timezone.now(),
    }
    return custom_export_report_by_name(
        "Pre-nomina", data, file="reporte", send_email=True
    )


def generar_reporte_certificados(modeladmin, request, queryset):
    # return redireccionar_a_vista_pdf("generar_reporte_certificados_view", queryset)
    entidades: List[SalarioMensualTotalPagado] = queryset.order_by("fecha")
    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.cargo,
            "ci": entidad.trabajador.carnet,
            "year": entidad.fecha.year,
            "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
            "mes": entidad.fecha.month,
            "Pago": float(entidad.pago_certificados_medicos),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "nombre_reporte": "Salario por Certificado",
        "fecha_imprecion": timezone.now(),
    }
    return custom_export_report_by_name(
        "Salario por Certificado", data, file="reporte", send_email=True
    )


def general_reporte_prestacion_social_pdf(modeladmin, request, queryset):
    # return redireccionar_a_vista_pdf("general_reporte_prestacion_social_view", queryset)

    entidades: List[PrestacionSocial] = PrestacionSocial.objects.filter(
        licencia_maternidad__in=queryset
    ).order_by("fecha_inicio")
    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.licencia_maternidad.trabajador.nombre,
            "apellidos": entidad.licencia_maternidad.trabajador.apellidos,
            "cargo": entidad.licencia_maternidad.trabajador.cargo,
            "ci": entidad.licencia_maternidad.trabajador.carnet,
            "inicio": entidad.fecha_inicio,
            "fin": entidad.fecha_fin,
            "Pago": float(entidad.prestacion_economica),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "nombre_reporte": "Salario de licencia por Maternidad",
        "fecha_imprecion": timezone.now(),
    }
    return custom_export_report_by_name(
        "Salario de licencia por Maternidad", data, file="reporte", send_email=True
    )


def generar_reporte_utilidades_pdf(modeladmin, request, queryset):
    # return redireccionar_a_vista_pdf("generar_reporte_utilidades_view", queryset)
    entidades: List[PagoPorUtilidadesAnuales] = queryset.order_by("fecha")

    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.cargo,
            "ci": entidad.trabajador.carnet,
            "year": entidad.fecha.year,
            "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
            "mes": entidad.fecha.month,
            "Pago": float(entidad.pago),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "nombre_reporte": "Salario de Utilidades Anuales",
        "fecha_imprecion": timezone.now(),
    }
    return custom_export_report_by_name(
        "Salario de Utilidades Anuales", data, file="reporte", send_email=True
    )


def generar_reporte_historial_de_evaluacion_pdf(modeladmin, request, queryset):
    # return redireccionar_a_vista_pdf(
    #     "generar_reporte_historial_de_evaluacion_view", queryset
    # )
    entidades: List[SalarioMensualTotalPagado] = queryset.order_by("fecha")
    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.cargo,
            "ci": entidad.trabajador.carnet,
            "year": entidad.fecha.year,
            "mes": entidad.fecha.month,
            "evaluacion": entidad.get_evalucacion_str(),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "nombre_reporte": "Historial de evaluación",
        "fecha_imprecion": timezone.now(),
    }
    # print(len(lista))
    return custom_export_report_by_name(
        "Historial de evaluación", data, file="reporte", send_email=True
    )
