import json
import os
from typing import Dict

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.storage import default_storage
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from apps.nomina.models import Trabajador,LicenciaPrenatal,LicenciaMaternidad,SegundaLicenciaPosnatal,PrestacionSocial,PrimeraLicenciaPosnatal,SalarioMensualTotalPagado,SalarioEscala,Asistencia

from apps.nomina.utils.util_salario import get_dias_laborales, es_viernes, get_first_day_of_last_30_months
from apps.nomina.utils.utils_ejemplos import obtener_fechas_ultimos_30_meses
import random

def mes_a_numero(mes):
    meses = {"enero": 1, "febrero": 2, "marzo": 3,
             "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
             "agosto": 8, "septiembre": 9, "octubre": 10,
             "noviembre": 11, "diciembre": 12}
    return meses.get(mes.lower(), "Mes no válido")
def get_date(date_string):
    return timezone.datetime.strptime(date_string, "%Y-%m-%d").date()
class TestSetUpEmpty(APITestCase):
    def tearDown(self):
        super().tearDown()
    def test_fechas_maternidad(self):
        salario_escala:SalarioEscala=SalarioEscala.objects.filter(grupo_escala="XXI",grupo_complejidad="VI").first()
        self.assertEqual(True, salario_escala is not None)
        self.assertEqual(11195, salario_escala.rango_salarial_5)
        trabajador = Trabajador.objects.first()
        fechas_dias=[]
        ultimos_30_meses =get_first_day_of_last_30_months()#obtener_fechas_ultimos_30_meses()
        for fecha in ultimos_30_meses:
            # print()
            dias_de_este_mes=get_dias_laborales(fecha.year,fecha.month)
            for fecha_dia_de_asitencia in dias_de_este_mes:
                # if fecha_dia_de_asitencia in fechas_dias:
                    # print(fecha_dia_de_asitencia)
                    # print(fechas_dias)
                self.assertEqual(False, fecha_dia_de_asitencia in fechas_dias)

                fechas_dias.append(fecha_dia_de_asitencia)
                self.assertEqual(True, fecha_dia_de_asitencia in fechas_dias)
                asisetencia=Asistencia()
                asisetencia.fecha=fecha_dia_de_asitencia
                asisetencia.horas_trabajadas=8 if es_viernes(fecha_dia_de_asitencia) else 9
                asisetencia.trabajador=trabajador
                asisetencia.save()

            salario = SalarioMensualTotalPagado()
            salario.evaluacion_obtenida_por_el_jefe="E"
            salario.evaluacion_obtenida_por_el_jefe_en_puntos=100
            salario.fecha = fecha
            salario.trabajador = trabajador
            salario.save()




        licencia_maternidad = LicenciaMaternidad()
        licencia_maternidad.trabajador = trabajador
        fecha_inicio = get_date("2024-05-12")
        licencia_maternidad.fecha_inicio = fecha_inicio
        licencia_maternidad.save()
        licencia_prenatal = LicenciaPrenatal()
        licencia_prenatal.licencia_maternidad = licencia_maternidad
        licencia_prenatal.fecha_inicio = fecha_inicio
        licencia_prenatal.fecha_fin = get_date("2024-06-26")
        licencia_prenatal.trabajador = trabajador
        licencia_prenatal.save()

        primera = PrimeraLicenciaPosnatal()
        primera.licencia_maternidad = licencia_maternidad
        primera.fecha_inicio = get_date("2024-06-26")
        primera.fecha_fin = get_date("2024-08-07")
        primera.save()

        segunda=SegundaLicenciaPosnatal.objects.filter(licencia_maternidad=licencia_maternidad).first()
        self.assertEqual(True, segunda is not None)
        self.assertEqual(segunda.fecha_inicio, get_date("2024-08-08"))
        self.assertEqual(segunda.fecha_fin, get_date("2024-09-19"))

        prestacion = PrestacionSocial.objects.filter(licencia_maternidad=licencia_maternidad).first()
        self.assertEqual(True, prestacion is not None)
        self.assertEqual(prestacion.fecha_inicio, get_date("2024-09-20"))
        self.assertEqual(prestacion.fecha_fin, get_date("2025-06-26"))
