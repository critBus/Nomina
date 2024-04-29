from django.utils import timezone

from datetime import timedelta

# def calcular_ISP(fecha, trabajador
# ):
#     fecha_limite_inferior = fecha - timezone.timedelta(days=365)
#     fecha_limite_inferior.replace(day=1)
#     SA = (
#         SalarioMensualTotalPagado.objects.filter(
#             fecha__gte=fecha_limite_inferior, trabajador=trabajador
#         )
#         .order_by("-fecha")[:12]
#         .aggregate(total=Sum("salario_basico_mensual"))["total"]
#     )
#     ISP = SA / 52
#     return ISP


def dias_entre_semana(fecha1, fecha2):
    if fecha1 == fecha2:
        return 0
    es_diferencia_positiva = fecha2 > fecha1
    fecha_mayor = fecha1 if es_diferencia_positiva else fecha2
    fecha_menor = fecha2 if es_diferencia_positiva else fecha1

    dias = 0
    while fecha_menor <= fecha_mayor:
        if fecha_menor.weekday() < 5:  # Si es un día de la semana (lunes a viernes)
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
    siguiente_dia = fecha_actual + timedelta(days=1)

    while siguiente_dia.weekday() < 5:
        siguiente_dia += timedelta(days=1)

    return siguiente_dia


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
