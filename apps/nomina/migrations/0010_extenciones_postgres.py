from django.contrib.postgres.operations import (
    BtreeGinExtension,
    BtreeGistExtension,
    CITextExtension,
    CryptoExtension,
    HStoreExtension,
    TrigramExtension,
    UnaccentExtension,
)
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("nomina", "0009_salariomensualtotalpagado_salario_anual_and_more"),
    ]
    operations = [
        TrigramExtension(),
        UnaccentExtension(),
        BtreeGinExtension(),
        BtreeGistExtension(),
        CITextExtension(),
        CryptoExtension(),
        HStoreExtension(),
    ]
