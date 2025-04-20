import traceback

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from apps.nomina.utils.utils_comencladores import (
        crear_roles_django_default,
        crear_salarios_escalas_default,
    )
from apps.nomina.utils.utils_ejemplos import (
    crear_dias_feriados_default,
    create_fake_trabajadores,
    create_usuarios_con_roles_default,
)
from apps.nomina.utils.util_email_reporte_d import load_automatic_reports
from django.conf import settings


def create_data():
    
    if settings.LOAD_EXAMPLE_DATA:
        load_automatic_reports()
        crear_salarios_escalas_default()
        crear_roles_django_default()

        create_usuarios_con_roles_default()
        crear_dias_feriados_default()
        create_fake_trabajadores()
        


class Command(BaseCommand):
    help = "Create All Tables"

    def handle(self, *args, **kwargs):
        try:
            create_data()

        except Exception:
            print(traceback.format_exc())