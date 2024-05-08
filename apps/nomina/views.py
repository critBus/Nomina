import json
from typing import List

from django.contrib.auth import logout

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_reportbroD.utils import export_report_by_name

from .models import *
from .utils.utils_reportes_d import generar_reporte_sbm


def generar_reporte_maternidad_view(request):
    query_param = request.GET.get("data_pdf")
    data = json.loads(query_param)
    # print(query_param)
    entidades: List[LicenciaMaternidad] = LicenciaMaternidad.objects.filter(
        id__in=data["lista_ids"]
    ).order_by("fecha_inicio")

    lista = []
    for licencia in entidades:
        data_licencia = {
            "nombre": licencia.trabajador.nombre,
            "apellidos": licencia.trabajador.apellidos,
            "ci": licencia.trabajador.carnet,
            "cargo": licencia.trabajador.salario_escala.grupo_escala,
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

    return export_report_by_name(
        "Control de la Prestación de Pago", data, extension="xlsx", file="reporte"
    )


def generar_reporte_sdm_view(request):
    query_param = request.GET.get("data_pdf")
    data = json.loads(query_param)
    # print(query_param)
    entidades: List[
        SalarioMensualTotalPagado
    ] = SalarioMensualTotalPagado.objects.filter(id__in=data["lista_ids"]).order_by(
        "fecha"
    )

    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.salario_escala.grupo_escala,
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
    }
    return export_report_by_name(
        "Salario Devengado", data, extension="pdf", file="reporte"
    )


def generar_reporte_sbm_view(request):
    query_param = request.GET.get("data_pdf")
    data = json.loads(query_param)
    # print(query_param)
    entidades: List[
        SalarioMensualTotalPagado
    ] = SalarioMensualTotalPagado.objects.filter(id__in=data["lista_ids"]).order_by(
        "fecha"
    )

    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.salario_escala.grupo_escala,
            "ci": entidad.trabajador.carnet,
            "year": entidad.fecha.year,
            "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
            "mes": entidad.fecha.month,
            "Pago": float(entidad.pago_total),
        }
        lista.append(data_entidad)

    data = {"lista": lista, "nombre_reporte": "Pre-nomina"}
    return export_report_by_name("Pre-nomina", data, extension="pdf", file="reporte")


def generar_reporte_certificados_view(request):
    query_param = request.GET.get("data_pdf")
    data = json.loads(query_param)
    # print(query_param)
    entidades: List[
        SalarioMensualTotalPagado
    ] = SalarioMensualTotalPagado.objects.filter(id__in=data["lista_ids"]).order_by(
        "fecha"
    )
    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.salario_escala.grupo_escala,
            "ci": entidad.trabajador.carnet,
            "year": entidad.fecha.year,
            "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
            "mes": entidad.fecha.month,
            "Pago": float(entidad.pago_certificados_medicos),
        }
        lista.append(data_entidad)

    data = {"lista": lista, "nombre_reporte": "Salario por Certificado"}
    return export_report_by_name(
        "Salario por Certificado", data, extension="pdf", file="reporte"
    )


def general_reporte_prestacion_social_view(request):
    query_param = request.GET.get("data_pdf")
    data = json.loads(query_param)
    # print(query_param)
    entidades: List[LicenciaMaternidad] = LicenciaMaternidad.objects.filter(
        id__in=data["lista_ids"]
    )
    entidades: List[PrestacionSocial] = PrestacionSocial.objects.filter(
        licencia_maternidad__in=entidades
    ).order_by("fecha_inicio")
    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.licencia_maternidad.trabajador.nombre,
            "apellidos": entidad.licencia_maternidad.trabajador.apellidos,
            "cargo": entidad.licencia_maternidad.trabajador.salario_escala.grupo_escala,
            "ci": entidad.licencia_maternidad.trabajador.carnet,
            "inicio": entidad.fecha_inicio,
            "fin": entidad.fecha_fin,
            "Pago": float(entidad.prestacion_economica),
        }
        lista.append(data_entidad)

    data = {"lista": lista, "nombre_reporte": "Salario de licencia por Maternidad"}
    return export_report_by_name(
        "Salario de licencia por Maternidad", data, extension="pdf", file="reporte"
    )


def generar_reporte_utilidades_view(request):
    query_param = request.GET.get("data_pdf")
    data = json.loads(query_param)
    # print(query_param)
    entidades: List[PagoPorUtilidadesAnuales] = PagoPorUtilidadesAnuales.objects.filter(
        id__in=data["lista_ids"]
    ).order_by("fecha")

    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.salario_escala.grupo_escala,
            "ci": entidad.trabajador.carnet,
            "year": entidad.fecha.year,
            "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
            "mes": entidad.fecha.month,
            "Pago": float(entidad.pago),
        }
        lista.append(data_entidad)

    data = {"lista": lista, "nombre_reporte": "Salario de Utilidades Anuales"}
    return export_report_by_name(
        "Salario de Utilidades Anuales", data, extension="pdf", file="reporte"
    )


def generar_reporte_historial_de_evaluacion_view(request):
    query_param = request.GET.get("data_pdf")
    data = json.loads(query_param)
    # print(query_param)
    entidades: List[
        SalarioMensualTotalPagado
    ] = SalarioMensualTotalPagado.objects.filter(id__in=data["lista_ids"]).order_by(
        "fecha"
    )
    lista = []
    for entidad in entidades:
        data_entidad = {
            "nombre": entidad.trabajador.nombre,
            "apellidos": entidad.trabajador.apellidos,
            "cargo": entidad.trabajador.salario_escala.grupo_escala,
            "ci": entidad.trabajador.carnet,
            "year": entidad.fecha.year,
            "mes": entidad.fecha.month,
            "evaluacion": entidad.get_evalucacion_str(),
        }
        lista.append(data_entidad)

    data = {
        "lista": lista,
        "nombre_reporte": "Historial de evaluación",
        # "fecha_imprecion":timezone.now(),
    }
    print(len(lista))
    return export_report_by_name(
        "Historial de evaluación", data, extension="pdf", file="reporte"
    )


# def reporte_view(request):
#     query_param = request.GET.get('data_pdf')
#     nombre_template = request.GET.get('nombre_template')
#     data = json.loads(query_param)
#     return export_report_by_name(
#         nombre_template, data, extension="pdf", file="reporte"
#     )
# return generar_reporte_sbm(None,request,SalarioMensualTotalPagado.objects.all())
