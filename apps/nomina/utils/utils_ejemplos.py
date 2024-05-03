from .util_salario import get_first_day_of_last_30_months, get_dias_laborales, es_viernes
from ..models import Trabajador, SalarioEscala, SalarioMensualTotalPagado, LicenciaMaternidad, LicenciaPrenatal, \
    PrimeraLicenciaPosnatal, SegundaLicenciaPosnatal, PrestacionSocial, Asistencia, CertificadoMedicoGeneral, \
    PrimerCertificadoMedico,ExtraCertificadoMedico
from faker import Faker
import random
from datetime import datetime, timedelta
from django.utils import timezone


fake = Faker()

def obtener_fechas_ultimos_30_meses():
    fechas = []


    fecha_actual = datetime.now()

    for i in range(1, 31):
        fecha = fecha_actual - timedelta(days=fecha_actual.day - 1) - timedelta(weeks=i * 4)
        fechas.append(fecha)

    return fechas
def create_fake_trabajadores(num_trabajadores=20):
    salarios = SalarioEscala.objects.all()
    if Trabajador.objects.count()==0 and salarios.count()>21:

        for i in range(num_trabajadores):
            # if i>1:
            #     break
            Trabajador.objects.create(
                carnet=fake.unique.numerify(text="############"),
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                categoria_ocupacional=fake.random_element(
                    elements=("Categoria1", "Categoria2")
                ),
                email=fake.email(),
                telefono=fake.unique.numerify(text="########"),
                direccion=fake.address(),
                area=fake.random_element(elements=("Economía", "Desarrollo", "Dirección")),
                salario_escala=salarios[random.randint(1, 20)],
            )
        evaluaciones=[
            ("E",100),
            ("E", 98),
            ("MB", 96),
            ("MB", 95),
            ("B", 88),
            ("B", 89),
        ]
        fechas_dias = []
        trabajadores=Trabajador.objects.all()
        ultimos_30_meses = get_first_day_of_last_30_months()
        for i,trabajador in enumerate(trabajadores):
            if i>15:
                break
            for fecha in ultimos_30_meses:
                # if fecha.year==2024 and fecha.month==7 and fecha.day==1:
                #     print("el dia que se exede")
                # if fecha.year==2024 and fecha.month==5 and fecha.day==13:
                #     print("el dia que se exede")
                dias_de_este_mes = get_dias_laborales(fecha.year, fecha.month)
                for fecha_dia_de_asitencia in dias_de_este_mes:


                    fechas_dias.append(fecha_dia_de_asitencia)
                    asisetencia = Asistencia()
                    asisetencia.fecha = fecha_dia_de_asitencia
                    asisetencia.horas_trabajadas = 8 if es_viernes(fecha_dia_de_asitencia) else 9
                    asisetencia.trabajador = trabajador
                    asisetencia.save()

                salario = SalarioMensualTotalPagado()
                evaluacion=evaluaciones[random.randint(0,len(evaluaciones)-1)]
                # salario.evaluacion_obtenida_por_el_jefe = evaluacion[0]
                salario.evaluacion_obtenida_por_el_jefe_en_puntos = evaluacion[1]
                salario.fecha = fecha
                salario.trabajador = trabajador
                salario.save()

            #ejemplo1
            # certificadogeneral = CertificadoMedicoGeneral()
            # certificadogeneral.descripcion = "la descripcion"
            # certificadogeneral.trabajador = trabajador
            # certificadogeneral.ingresado = random.randint(1, 3) == 2
            # certificadogeneral.save()


            # certificado=CertificadoMedico()
            # certificado.certificado_medico_general=certificadogeneral
            # certificado.fecha_inicio=timezone.now()
            # certificado.fecha_fin=certificado.fecha_inicio+timedelta(weeks=random.randint(5,8))
            # certificado.save()

            # ultima_fecha=certificado.fecha_fin
            
            # certificado2 = CertificadoMedico()
            # certificado2.certificado_medico_general = certificadogeneral
            # certificado2.fecha_inicio = ultima_fecha+timedelta(days=1)
            # certificado2.fecha_fin = certificado.fecha_inicio + timedelta(weeks=random.randint(5, 8))
            # certificado2.save()
            #fin ejemplo1



        for i,trabajador in enumerate(trabajadores):
            if i<5:
                licencia_maternidad=LicenciaMaternidad()
                licencia_maternidad.trabajador=trabajador
                mes=24+random.randint(1, 5)
                # print(f"mes {mes}")
                # print(ultimos_30_meses)
                fecha_inicio=ultimos_30_meses[mes]
                # print(f"fecha_incio {fecha_inicio}")
                licencia_maternidad.fecha_inicio=fecha_inicio
                licencia_maternidad.save()
                licencia_prenatal=LicenciaPrenatal()
                licencia_prenatal.licencia_maternidad=licencia_maternidad
                licencia_prenatal.fecha_inicio=fecha_inicio
                licencia_prenatal.fecha_fin=fecha_inicio + timedelta(weeks=48)
                licencia_prenatal.trabajador=trabajador
                licencia_prenatal.save()
                if random.randint(1,3)==2:

                    primera=PrimeraLicenciaPosnatal()
                    primera.licencia_maternidad=licencia_maternidad
                    primera.fecha_inicio=fecha_inicio + timedelta(weeks=45)
                    primera.fecha_fin=primera.fecha_inicio + timedelta(weeks=6)
                    primera.save()
            if i>5 and i<10:
                certificadogeneral = CertificadoMedicoGeneral()
                certificadogeneral.descripcion = "la descripcion"
                certificadogeneral.trabajador = trabajador
                certificadogeneral.ingresado = random.randint(1, 3) == 2
                certificadogeneral.save()


                certificado=PrimerCertificadoMedico()
                certificado.certificado_medico_general=certificadogeneral
                certificado.fecha_inicio=timezone.now()
                certificado.fecha_fin=certificado.fecha_inicio+timedelta(weeks=random.randint(5,8))
                certificado.save()

                ultima_fecha=certificado.fecha_fin
                for j in range(random.randint(0, 2)):
                    certificado2 = ExtraCertificadoMedico()
                    certificado2.certificado_medico_general = certificadogeneral
                    certificado2.fecha_inicio = ultima_fecha+timedelta(days=1)
                    certificado2.fecha_fin = certificado.fecha_inicio + timedelta(weeks=random.randint(5, 8))
                    certificado2.save()




