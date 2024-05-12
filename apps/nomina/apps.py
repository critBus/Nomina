from django.apps import AppConfig
from django.db.models.signals import post_migrate


def config_app(sender, **kwargs):
    from .utils.utils_comencladores import (
        crear_roles_django_default,
        crear_salarios_escalas_default,
    )
    from .utils.utils_ejemplos import (
        crear_dias_feriados_default,
        create_fake_trabajadores,
        create_usuarios_con_roles_default,
    )

    crear_salarios_escalas_default()
    crear_roles_django_default()

    create_usuarios_con_roles_default()
    crear_dias_feriados_default()
    create_fake_trabajadores()


class NominaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.nomina"

    def ready(self):
        post_migrate.connect(config_app, sender=self)
