import json
from typing import List

from django.shortcuts import redirect
from django.urls import reverse
from django_reportbroD.reportcore import reportPDF
from django_reportbroD.utils import export_report_by_name

from ..models import *

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
    return redireccionar_a_vista_pdf("generar_reporte_maternidad_view", queryset)
    # licencias:List[LicenciaMaternidad] = queryset
    # lista=[]
    # for licencia in licencias:
    #     data_licencia={"nombre": licencia.trabajador.nombre,
    #          "apellidos": licencia.trabajador.apellidos,
    #                    "ci":licencia.trabajador.carnet,
    #          "cargo": licencia.trabajador.salario_escala.grupo_escala,
    #          }
    #     pre:LicenciaPrenatal=LicenciaPrenatal.objects.filter(licencia_maternidad=licencia).first()
    #     data_licencia["Lic_Pre"]=float(pre.prestacion_economica) if pre else None
    #     pre: PrimeraLicenciaPosnatal = PrimeraLicenciaPosnatal.objects.filter(licencia_maternidad=licencia).first()
    #     data_licencia["Lic_Pos_1"] = float(pre.prestacion_economica) if pre else None
    #     pre: SegundaLicenciaPosnatal = SegundaLicenciaPosnatal.objects.filter(licencia_maternidad=licencia).first()
    #     data_licencia["Lic_Pos_2"] = float(pre.prestacion_economica) if pre else None
    #     lista.append(data_licencia)
    #
    # data = {
    #     "lista": lista,
    #     "nombre_reporte":"Control de la Prestación de Pago"
    # }
    # return redireccionar_a_vista_pdf( "Control de la Prestación de Pago", data)
    # data_pdf = json.dumps(data)
    # nombre_plantilla="Control de la Prestación de Pago"
    # url = reverse('generalpdf')+f"?nombre_template={nombre_plantilla}&data_pdf={data_pdf}"
    # print(url)
    # # Redireccionar al otro método y pasarle los datos
    # return redirect(url)
    # return export_report_by_name(
    #     "Control de la Prestación de Pago", data, extension="xlsx", file="reporte"
    # )
    # return reportPDF(request, code_report, data, file="reporte trabajadores")


def generar_reporte_sdm(modeladmin, request, queryset):
    return redireccionar_a_vista_pdf("generar_reporte_sdm_view", queryset)
    # entidades:List[SalarioMensualTotalPagado] = queryset
    # lista=[]
    # for entidad in entidades:
    #     data_entidad={"nombre": entidad.trabajador.nombre,
    #          "apellidos": entidad.trabajador.apellidos,
    #          "cargo": entidad.trabajador.salario_escala.grupo_escala,
    #           "ci": entidad.trabajador.carnet,
    #           "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
    #            "year":entidad.fecha.year,
    #            "mes": entidad.fecha.month,
    #            "Pago":float(entidad.salario_devengado_mensual),
    #
    #          }
    #     lista.append(data_entidad)
    #
    #
    # data = {
    #     "lista": lista,
    #     "nombre_reporte":"Salario Devengado",
    #
    # }
    # return redireccionar_a_vista_pdf( "Salario Devengado", data)
    # return export_report_by_name(
    #     "Salario Devengado", data, extension="pdf", file="reporte"
    # )


def generar_reporte_sbm(modeladmin, request, queryset):
    return redireccionar_a_vista_pdf("generar_reporte_sbm_view", queryset)
    # entidades:List[SalarioMensualTotalPagado] = queryset
    # lista=[]
    # for entidad in entidades:
    #     data_entidad={"nombre": entidad.trabajador.nombre,
    #          "apellidos": entidad.trabajador.apellidos,
    #          "cargo": entidad.trabajador.salario_escala.grupo_escala,
    #             "ci": entidad.trabajador.carnet,
    #            "year":entidad.fecha.year,
    #             "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
    #            "mes": entidad.fecha.month,
    #            "Pago":float(entidad.pago_total)
    #          }
    #     lista.append(data_entidad)
    #
    #
    # data = {
    #     "lista": lista,
    #     "nombre_reporte":"Pre-nomina"
    # }
    # return redireccionar_a_vista_pdf("Pre-nomina", data)
    # return export_report_by_name(
    #     "Pre-nomina", data, extension="pdf", file="reporte"
    # )


def generar_reporte_certificados(modeladmin, request, queryset):
    return redireccionar_a_vista_pdf("generar_reporte_certificados_view", queryset)
    # entidades:List[SalarioMensualTotalPagado] = queryset
    # # lista=[]
    # # for entidad in entidades:
    # #     data_entidad={"nombre": entidad.trabajador.nombre,
    # #          "apellidos": entidad.trabajador.apellidos,
    # #          "cargo": entidad.trabajador.salario_escala.grupo_escala,
    # #             "ci": entidad.trabajador.carnet,
    # #            "year":entidad.fecha.year,
    # #             "year_mes": f"{entidad.fecha.year}-{entidad.fecha.month}",
    # #            "mes": entidad.fecha.month,
    # #            "Pago":float(entidad.pago_certificados_medicos)
    # #          }
    # #     lista.append(data_entidad)
    #
    # data_pdf = json.dumps({
    #     "lista_ids":[v.id for v in entidades]
    # })
    # url = reverse('generalpdf') + f"?data_pdf={data_pdf}"#nombre_template={nombre_plantilla}&
    # # print(url)
    # return redirect(url)

    # data = {
    #     "lista": lista,
    #     "nombre_reporte":"Salario por Certificado"
    # }
    # return redireccionar_a_vista_pdf("Salario por Certificado", data)
    # return export_report_by_name(
    #     "Salario por Certificado", data, extension="pdf", file="reporte"
    # )


def general_reporte_prestacion_social_pdf(modeladmin, request, queryset):
    return redireccionar_a_vista_pdf("general_reporte_prestacion_social_view", queryset)


def generar_reporte_utilidades_pdf(modeladmin, request, queryset):
    return redireccionar_a_vista_pdf("generar_reporte_utilidades_view", queryset)


def generar_reporte_historial_de_evaluacion_pdf(modeladmin, request, queryset):
    return redireccionar_a_vista_pdf(
        "generar_reporte_historial_de_evaluacion_view", queryset
    )
