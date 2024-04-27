from ..models import SalarioEscala


def crear_salarios_escalas_default():
    datos = (
        ("IX", (11000, 11200, 11400, 11700, 12000)),
        ("XXIV", (10900, 11095, 11295, 11595, 11900)),
        ("XXIII", (10800, 10995, 11195, 11485, 11840)),
        ("XXI", (10200, 10385, 10570, 10845, 11195)),
        ("XX", (9870, 10050, 10230, 10500, 10760)),
        ("XIX", (9400, 9570, 9740, 10000, 10240)),
        ("XVIII", (8955, 9120, 9280, 9525, 9740)),
        ("XVII", (8530, 8685, 8840, 9075, 9300)),
        ("XVI", (8120, 8270, 8415, 8635, 8890)),
        ("XV", (7735, 7875, 8015, 8225, 8490)),
        ("XIV", (7365, 7500, 7663, 7835, 8110)),
        ("XIII", (7015, 7145, 7270, 7460, 7755)),
        ("XII", (6680, 6800, 6925, 7105, 7385)),
        ("XI", (6365, 6480, 6595, 6770, 7035)),
        ("X", (6090, 6170, 6280, 6445, 6700)),
        ("IX", (5770, 5875, 5980, 6135, 6375)),
        ("VI", (4985, 5075, 5165, 5300, 5510)),
        ("V", (4750, 4835, 4925, 5050, 5250)),
        ("IV", (4525, 4605, 4690, 4815, 5000)),
        ("III", (4305, 4385, 4460, 4585, 4760)),
        ("II", (4100, 4175, 4250, 4360, 4530)),
    )
    grupos_complejidad = (
        (
            "I",
            (
                "II",
                "III",
                "IV",
                "V",
                "VI",
            ),
        ),
        (
            "II",
            (
                "III",
                "IV",
                "V",
                "VI",
            ),
        ),
        (
            "III",
            (
                "IX",
                "X",
                "XI",
                "XII",
                "XIII",
                "XIV",
                "XV",
                "XVI",
                "XVII",
            ),
        ),
        (
            "IV",
            (
                "XVII",
                "XVIII",
                "XIX",
            ),
        ),
        (
            "V",
            (
                "IX",
                "X",
                "XI",
                "XII",
                "XIII",
                "XIV",
                "XV",
                "XVI",
                "XVII",
            ),
        ),
        (
            "IV",
            (
                "XVII",
                "XVIII",
                "XIX",
            ),
        ),
        (
            "VI",
            (
                "XIX",
                "XX",
                "XXI",
                "XXII",
                "XXIII",
                "XXIV",
                "XXV",
            ),
        ),
    )

    def get_rango_salarios(rango):
        respuesta = []
        for v in datos:
            if v[0] == rango:
                respuesta.append(v)
                break
        return respuesta

    def crear_salarios_escalas(
        grupo_complejidad, rango_salarial, grupo_escala, salario
    ):
        if not SalarioEscala.objects.filter(
            grupo_complejidad=grupo_complejidad,
            grupo_escala=grupo_escala,
            rango_salarial=rango_salarial,
        ).exists():
            salario_escala = SalarioEscala()
            salario_escala.grupo_complejidad = grupo_complejidad
            salario_escala.grupo_escala = grupo_escala
            salario_escala.rango_salarial = rango_salarial
            salario_escala.salario = salario
            salario_escala.save()

    for complejidad, rangos in grupos_complejidad:
        datos_actuales = []
        for rango in rangos:
            datos_actuales += get_rango_salarios(rango)

        for i, v in enumerate(datos_actuales):
            grupo_escala = v[0]
            for j, salario in enumerate(v[1]):
                grupo_complejidad = complejidad
                rango_salarial = j + 1
                crear_salarios_escalas(
                    grupo_complejidad, rango_salarial, grupo_escala, salario
                )
