from django.apps import AppConfig
from django.db.models.signals import post_migrate


def config_app(sender, **kwargs):
    from .utils.utils_comencladores import crear_salarios_escalas_default

    crear_salarios_escalas_default()


class NominaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.nomina"

    def ready(self):
        post_migrate.connect(config_app, sender=self)
