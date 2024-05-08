from django.urls import path

from .views import *

urlpatterns = [
    path(
        "generar_reporte_maternidad_view/",
        generar_reporte_maternidad_view,
        name="generar_reporte_maternidad_view",
    ),
    path(
        "generar_reporte_sdm_view/",
        generar_reporte_sdm_view,
        name="generar_reporte_sdm_view",
    ),
    path(
        "generar_reporte_sbm_view/",
        generar_reporte_sbm_view,
        name="generar_reporte_sbm_view",
    ),
    path(
        "generar_reporte_certificados_view/",
        generar_reporte_certificados_view,
        name="generar_reporte_certificados_view",
    ),
    path(
        "general_reporte_prestacion_social_view/",
        general_reporte_prestacion_social_view,
        name="general_reporte_prestacion_social_view",
    ),
    path(
        "generar_reporte_utilidades_view/",
        generar_reporte_utilidades_view,
        name="generar_reporte_utilidades_view",
    ),
    path(
        "generar_reporte_historial_de_evaluacion_view/",
        generar_reporte_historial_de_evaluacion_view,
        name="generar_reporte_historial_de_evaluacion_view",
    ),
]
