import random
from datetime import datetime, timedelta
from typing import List

from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from faker import Faker

from apps.users.models import User
from config.utils.utils_fechas import get_first_day_of_last_months

from ..models import (
    NOMBRE_CARGO_DIRECTOR,
    NOMBRE_ROL_ADMINISTRADOR,
    NOMBRE_ROL_TRABAJADOR,
    Asistencia,
    CertificadoMedicoGeneral,
    DiaFeriado,
    ExtraCertificadoMedico,
    LicenciaMaternidad,
    LicenciaPrenatal,
    PagoPorUtilidadesAnuales,
    PlanificacionUtilidadesAnuales,
    PrestacionSocial,
    PrimeraLicenciaPosnatal,
    PrimerCertificadoMedico,
    SalarioEscala,
    SalarioMensualTotalPagado,
    SegundaLicenciaPosnatal,
    Trabajador,
    es_viernes,
    get_dias_laborales,
)

DIAS_FERIADOS = (
    (2021, 1, 1, "Año Nuevo", "Inicio del nuevo año."),
    (2021, 4, 2, "Viernes Santo", "Celebración religiosa previa a la Pascua."),
    (2021, 5, 1, "Día del Trabajo", "Conmemoración de los derechos laborales."),
    (
        2021,
        9,
        15,
        "Día de la Independencia",
        "Celebración de la independencia nacional.",
    ),
    (2021, 12, 25, "Navidad", "Celebración religiosa del nacimiento de Jesús."),
    (2022, 1, 1, "Año Nuevo", "Comienzo del nuevo año."),
    (2022, 4, 15, "Viernes Santo", "Día de conmemoración religiosa."),
    (2022, 5, 1, "Día del Trabajo", "Reconocimiento a los derechos laborales."),
    (2022, 9, 15, "Día de la Independencia", "Celebración de la soberanía nacional."),
    (2022, 12, 25, "Navidad", "Festividad religiosa de la natividad de Jesús."),
    (2023, 1, 1, "Año Nuevo", "Inicio del año calendario."),
    (2023, 4, 7, "Viernes Santo", "Día de reflexión religiosa."),
    (2023, 5, 1, "Día del Trabajo", "Reconocimiento a la labor y derechos laborales."),
    (2023, 9, 15, "Día de la Independencia", "Celebración de la autonomía nacional."),
    (2023, 12, 25, "Navidad", "Celebración religiosa del nacimiento de Cristo."),
    (2024, 1, 1, "Año Nuevo", "Inicio del nuevo año."),
    (2024, 4, 1, "Viernes Santo", "Día de conmemoración religiosa."),
    (2024, 5, 1, "Día del Trabajo", "Reconocimiento a los derechos laborales."),
    (
        2024,
        9,
        15,
        "Día de la Independencia",
        "Celebración de la independencia nacional.",
    ),
    (2024, 12, 25, "Navidad", "Festividad religiosa del nacimiento de Jesús."),
)
fake = Faker()


def crear_dias_feriados_default():  # datos_dia_feriado
    if DiaFeriado.objects.count() == 0:
        for year, mes, dia, nombre, descripcion in DIAS_FERIADOS:
            dia_feriado = DiaFeriado()
            dia_feriado.fecha = timezone.now().replace(year=year, month=mes, day=dia)
            dia_feriado.nombre = nombre
            dia_feriado.descripcion = descripcion
            dia_feriado.save()


def obtener_fechas_ultimos_30_meses():
    fechas = []

    fecha_actual = datetime.now()

    for i in range(1, 31):
        fecha = (
            fecha_actual - timedelta(days=fecha_actual.day - 1) - timedelta(weeks=i * 4)
        )
        fechas.append(fecha)

    return fechas


def create_usuarios_con_roles_default():
    if User.objects.count() < 2:
        usuario_administrador = User.objects.create_user(
            username="administrador",
            email="administrador@gmail.com",
            first_name="administrador",
            last_name="administrador",
            password="123",
        )
        usuario_administrador.is_staff = True
        usuario_administrador.groups.add(
            Group.objects.get(name=NOMBRE_ROL_ADMINISTRADOR)
        )
        usuario_administrador.save()
        usuario_trabajador = User.objects.create_user(
            username="trabajador",
            email="trabajador@gmail.com",
            first_name="trabajador",
            last_name="trabajador",
            password="123",
        )
        usuario_trabajador.is_staff = True
        usuario_trabajador.groups.add(Group.objects.get(name=NOMBRE_ROL_TRABAJADOR))
        usuario_trabajador.save()


def create_fake_trabajadores(num_trabajadores=20):
    salarios = SalarioEscala.objects.all()
    if Trabajador.objects.count() == 0 and salarios.count() > 21:
        limite = 15
        for i in range(num_trabajadores):
            # if i>1:
            #     break
            femenino = random.randint(1, 3) == 2
            Trabajador.objects.create(
                carnet=fake.unique.numerify(text="############")[:11],
                nombre=fake.first_name() if not femenino else fake.first_name_female(),
                apellidos=fake.last_name(),
                categoria_ocupacional=fake.random_element(
                    elements=("Categoria1", "Categoria2")
                ),
                email=fake.email(),
                cargo=("Jefe" if random.randint(1, 5) == 3 else "Trabajador")
                if i != 0
                else NOMBRE_CARGO_DIRECTOR,
                sexo="Femenino" if femenino else "Masculino",
                telefono=fake.unique.numerify(text="########"),
                direccion=fake.address(),
                area=fake.random_element(
                    elements=("Economía", "Desarrollo", "Dirección")
                ),
                salario_escala=salarios[random.randint(1, 20)],
            )
        evaluaciones = [
            ("E", 100),
            ("E", 98),
            ("MB", 96),
            ("MB", 95),
            ("B", 88),
            ("B", 89),
        ]
        fechas_dias = []
        trabajadores: List[Trabajador] = Trabajador.objects.all()
        ultimos_30_meses = get_first_day_of_last_months(
            30
        )  # get_first_day_of_last_30_months()
        lista_salarios = []
        for i, trabajador in enumerate(trabajadores):
            if i > limite:
                break
            for fecha in ultimos_30_meses[3:]:
                # if fecha.year==2024 and fecha.month==7 and fecha.day==1:
                #     print("el dia que se exede")
                # if fecha.year==2024 and fecha.month==5 and fecha.day==13:
                #     print("el dia que se exede")
                dias_de_este_mes = get_dias_laborales(fecha.year, fecha.month)
                for fecha_dia_de_asitencia in dias_de_este_mes:
                    fechas_dias.append(fecha_dia_de_asitencia)
                    asisetencia = Asistencia()
                    asisetencia.fecha = fecha_dia_de_asitencia
                    asisetencia.horas_trabajadas = (
                        8 if es_viernes(fecha_dia_de_asitencia) else 9
                    )
                    asisetencia.trabajador = trabajador
                    asisetencia.save()

                salario = SalarioMensualTotalPagado()
                evaluacion = evaluaciones[random.randint(0, len(evaluaciones) - 1)]
                # salario.evaluacion_obtenida_por_el_jefe = evaluacion[0]
                salario.evaluacion_obtenida_por_el_jefe_en_puntos = evaluacion[1]
                salario.fecha = fecha
                salario.trabajador = trabajador
                salario.save()
                lista_salarios.append(salario)

        dinero_a_repartir = 15000 * len(trabajadores)
        planificacion_utilidades = PlanificacionUtilidadesAnuales()
        planificacion_utilidades.dinero_a_repartir = dinero_a_repartir
        planificacion_utilidades.fecha = timezone.now()
        planificacion_utilidades.year = planificacion_utilidades.fecha.year - 1
        planificacion_utilidades.save()

        cantidad = 0
        for i, trabajador in enumerate(trabajadores):
            if cantidad < 5 and trabajador.sexo == "Femenino":
                cantidad += 1
                licencia_maternidad = LicenciaMaternidad()
                licencia_maternidad.trabajador = trabajador
                mes = 24 + random.randint(1, 5)
                # print(f"mes {mes}")
                # print(ultimos_30_meses)
                fecha_inicio = ultimos_30_meses[mes]
                # print(f"fecha_incio {fecha_inicio}")
                licencia_maternidad.fecha_inicio = fecha_inicio
                licencia_maternidad.save()
                licencia_prenatal = LicenciaPrenatal()
                licencia_prenatal.licencia_maternidad = licencia_maternidad
                licencia_prenatal.fecha_inicio = fecha_inicio
                licencia_prenatal.fecha_fin = fecha_inicio + timedelta(weeks=48)
                licencia_prenatal.trabajador = trabajador
                licencia_prenatal.save()
                if random.randint(1, 3) == 2:
                    primera = PrimeraLicenciaPosnatal()
                    primera.licencia_maternidad = licencia_maternidad
                    primera.fecha_inicio = fecha_inicio + timedelta(weeks=45)
                    primera.fecha_fin = primera.fecha_inicio + timedelta(weeks=6)
                    primera.save()

        for i, trabajador in enumerate(trabajadores):
            if i > 5 and i < 10:
                certificadogeneral = CertificadoMedicoGeneral()
                certificadogeneral.descripcion = "la descripcion"
                certificadogeneral.trabajador = trabajador
                certificadogeneral.ingresado = random.randint(1, 3) == 2
                certificadogeneral.save()

                certificado = PrimerCertificadoMedico()
                certificado.certificado_medico_general = certificadogeneral
                certificado.fecha_inicio = timezone.now()
                certificado.fecha_fin = certificado.fecha_inicio + timedelta(
                    weeks=random.randint(5, 8)
                )
                certificado.save()

                ultima_fecha = certificado.fecha_fin
                for j in range(random.randint(0, 2)):
                    certificado2 = ExtraCertificadoMedico()
                    certificado2.certificado_medico_general = certificadogeneral
                    certificado2.fecha_inicio = ultima_fecha + timedelta(days=1)
                    certificado2.fecha_fin = certificado.fecha_inicio + timedelta(
                        weeks=random.randint(5, 8)
                    )
                    certificado2.save()

        for salario in lista_salarios:
            salario.save()
