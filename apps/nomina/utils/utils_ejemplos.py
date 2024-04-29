from ..models import Trabajador, SalarioEscala, SalarioMensualTotalPagado, LicenciaMaternidad, LicenciaPrenatal,PrimeraLicenciaPosnatal,SegundaLicenciaPosnatal,PrestacionSocial
from faker import Faker
import random
from datetime import datetime, timedelta



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

        for _ in range(num_trabajadores):
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

        ultimos_30_meses =obtener_fechas_ultimos_30_meses()
        trabajadores=Trabajador.objects.all()
        for trabajador in trabajadores:
            for fecha in ultimos_30_meses:
                salario=SalarioMensualTotalPagado()
                salario.salario_basico_mensual=trabajador.salario_escala.salario
                salario.salario_devengado_mensual=salario.salario_basico_mensual+random.randint(1, 1000)
                salario.fecha=fecha
                salario.trabajador=trabajador
                salario.save()

        for i,trabajador in enumerate(trabajadores):
            if i<10:
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




