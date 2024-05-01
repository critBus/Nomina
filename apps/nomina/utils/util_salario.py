from django.utils import timezone


from datetime import datetime, timedelta,date
# mes - dia
DIAS_FERIADOS =(
    (5,(1,)),
    (7,(26,)),
)
def es_dia_feriado(fecha:date):
    for mes, dias in DIAS_FERIADOS:
        if fecha.month == mes:
            if fecha.day in dias:
                return True
    return False
def get_dias_feriado(mes_a_buscar):
    for mes, dias in DIAS_FERIADOS:
        if mes_a_buscar== mes:
            return dias
    return []


def get_days_in_month(year, month):
    start_date = datetime(year, month, 1)
    end_date = start_date.replace(month=start_date.month % 12 + 1, day=1) - timedelta(days=1)

    days = [(start_date + timedelta(days=i)).date() for i in range((end_date - start_date).days + 1)]
    days=list(set(days))
    # days.sort()
    # print(f"{days[0].month if days else '-'} {days[0].year if days else '-'}  {[v.day for v in days]}")

    return days

def get_dias_laborales(year, month):
    seleccionados=[]
    dias=get_days_in_month(year, month)
    for dia in dias:
        if es_dia_entresemana(dia) and not es_dia_feriado(dia):
            seleccionados.append(dia)
    # todos los dias entre semana menos los feriados
    return seleccionados


def get_dias_entre_semana(fecha1, fecha2):
    if fecha1 == fecha2:
        return 0
    es_diferencia_positiva = fecha2 > fecha1
    fecha_mayor = fecha1 if es_diferencia_positiva else fecha2
    fecha_menor = fecha2 if es_diferencia_positiva else fecha1

    dias = 0
    while fecha_menor <= fecha_mayor:
        if es_dia_entresemana(fecha_menor):  # Si es un día de la semana (lunes a viernes)
            dias += 1
        fecha_menor += timedelta(days=1)
    if not es_diferencia_positiva:
        dias *= -1
    return dias


def veces_supera_siete(dias):
    veces = dias // 7
    if dias % 7 != 0:
        veces += 1
    return abs(veces)


def misma_semana(fecha1, fecha2):
    if fecha1.isocalendar()[1] == fecha2.isocalendar()[1]:
        return True
    else:
        return False


def dias_restantes_mes(fecha):
    # Obtener el último día del mes
    ultimo_dia_mes = fecha.replace(day=1, month=fecha.month % 12 + 1) - timedelta(
        days=1
    )

    # Calcular la diferencia en días entre la fecha dada y el último día del mes
    dias_restantes = (ultimo_dia_mes - fecha).days

    return dias_restantes


def sumar_semanas(fecha, semanas):
    nueva_fecha = fecha + timedelta(weeks=semanas)

    return nueva_fecha


def siguiente_dia_laborable(fecha_actual):
    # nombre_dia_semana(fecha_actual)
    siguiente_dia = fecha_actual + timedelta(days=1)

    while not es_dia_entresemana(siguiente_dia):
        siguiente_dia += timedelta(days=1)

    # nombre_dia_semana(siguiente_dia)
    return siguiente_dia

def es_dia_entresemana(fecha):
    return fecha.weekday() < 5
def es_viernes(fecha):
    return fecha.weekday()==4
def primer_cumpleannos(fecha_nacimiento):
    anno_nacimiento = fecha_nacimiento.year
    primer_cumpleannos = fecha_nacimiento.replace(year=anno_nacimiento + 1)
    return primer_cumpleannos


def diferencia_menos_de_5_meses(fecha1, fecha2):
    diferencia_meses = abs(
        (fecha1.year - fecha2.year) * 12 + fecha1.month - fecha2.month
    )

    if diferencia_meses < 5:
        return True
    else:
        return False


def nombre_dia_semana(fecha):
    dias_semana = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo"
    }

    try:
        dia_semana = fecha.weekday()
        print(f"fecha: {fecha}")
        print(f"El día de la semana es: {dias_semana[dia_semana]}")
    except ValueError:
        print("Formato de fecha incorrecto. Debe ser en el formato YYYY-MM-DD.")

def get_first_day_of_last_months(cantidad_de_meses):

    """
    Devuelve una lista con el primer día de cada mes de los últimos 30 meses.

    Returns:
        list: Una lista de objetos date que representan el primer día de cada mes de los últimos 30 meses.
    """
    today = date.today()
    first_days = []

    for i in range(30):
        # first_day = date(today.year - (i // 12), today.month - (i % 12) , 1)#+ 1
        try:
            first_day = date(today.year - (i // 12),  ((today.month + i) % 12)+1 , 1)#+ 1
        except:
            print(f"i={i} {today.month} {i % 12} {((today.month + i) % 12)+1 }") #+ 1
            assert False
        first_days.append(first_day)

    return first_days

def get_first_day_of_last_30_months():
    return get_first_day_of_last_months(30)