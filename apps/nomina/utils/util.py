

#
# def semanas_laborales_embarazo(inicio_embarazo, fin_embarazo):
#     # Calcular la fecha en que le tocaba el parto
#     fecha_parto_prevista = inicio_embarazo + timedelta(days=280)
#
#     # Calcular la diferencia entre la fecha de parto prevista y la fecha de parto real
#     diferencia_dias = (fin_embarazo - fecha_parto_prevista).days
#
#     # Contar los días laborales en la diferencia de fechas
#     dias_laborales = 0
#     current_date = fecha_parto_prevista
#     while current_date <= fin_embarazo:
#         if current_date.weekday() < 5:  # 0 es lunes, 4 es viernes
#             dias_laborales += 1
#         current_date += timedelta(days=1)
#
#     # Calcular las semanas laborales (considerando 5 días laborales por semana)
#     semanas_laborales = dias_laborales // 7  # 5
#
#     return semanas_laborales
