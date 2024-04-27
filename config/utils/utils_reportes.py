import io
from io import BytesIO

# Create your views here.
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Dict,
    List,
    NoReturn,
    Optional,
    Tuple,
    Union,
    cast,
)

from django.conf import settings
from django.db.models import Q
from django.shortcuts import HttpResponse, render
from django.views.generic import View
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle


class DatosColumnaReporte:
    def __init__(self):
        self.header = ""
        self.metodo_getValor = None
        self.proporcion_comlumna = 1


class AdministradorDeReporte:
    def __init__(self):
        self.columnas: List[DatosColumnaReporte] = []
        self.titulo = ""
        self.claseModelo = None
        self.dic_campo_atributo = {}
        self.dic_campo_metodo_filtrar = {}

    def setClaseModelo(self, claseModelo):
        self.claseModelo = claseModelo
        self.dic_campo_atributo = {str(v): str(v) for v in vars(claseModelo)}

    def add(self, header, metodo_getValor, proporcion_comlumna=1):
        d = DatosColumnaReporte()
        d.header = header
        d.metodo_getValor = metodo_getValor
        d.proporcion_comlumna = proporcion_comlumna
        self.columnas.append(d)
        return self

    def getAction(self):
        def metodoAction(modeladmin, request, queryset):
            response = HttpResponse(content_type="application/pdf")
            buff = io.BytesIO()
            doc = SimpleDocTemplate(
                buff,
                pagesize=landscape(letter),
                rightMargin=40,
                leftMargin=40,
                topMargin=60,
                bottomMargin=18,
            )
            categorias = []
            styles = getSampleStyleSheet()
            header = Paragraph(self.titulo, styles["Heading1"])
            categorias.append(header)

            # ------------------
            encabezados = (v.header for v in self.columnas)

            def getL(z):
                return [v.metodo_getValor(z) for v in self.columnas]

            def p(v):
                if isinstance(v, int) or isinstance(v, float):
                    return v
                return Paragraph(
                    str(v)
                )  # Paragraph('<font size=' + str(self.FontSise) + '>' + str(v) + "</font>")  # <center>

            # Creamos una lista de tuplas que van a contener a las personas
            detalles = [
                tuple(p(e) for e in getL(v))
                for v in queryset  # InstitucionProductiva.objects.all()
            ]
            # ------------------
            # headings = ('Id', 'Descrición', 'Activo', 'Creación')

            # todascategorias = [(p.id, p.descripcion, p.activo, p.creado)for p in Categoria.objects.all().order_by('pk')]

            t = Table([encabezados] + detalles)
            t.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("GRID", (0, 0), (-1, -1), 1, colors.dodgerblue),
                        ("LINEBELOW", (0, 0), (-1, 0), 2, colors.darkblue),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.dodgerblue),
                    ]
                )
            )

            categorias.append(t)
            doc.build(categorias)
            response.write(buff.getvalue())
            buff.close()
            return response

        metodoAction.short_description = "Exportar a PDF"
        return metodoAction

    def filtrar(self, request):
        q = request.GET.get("q")
        campo = request.GET.get("campo")
        queryset = None
        if q and campo:
            q = q.strip()
            if campo in self.dic_campo_metodo_filtrar:
                queryset = self.dic_campo_metodo_filtrar[campo](self, q, campo)
            elif campo in self.dic_campo_atributo:
                valor = self.dic_campo_atributo[campo]
                filtro = str(valor + "__icontains")
                queryset = self.claseModelo.objects.filter(**{filtro: q})
        else:
            queryset = self.claseModelo.objects.all()
        return queryset

    def getView(self):
        def metodoView(request):
            return self.getAction()(None, None, self.filtrar(request))

        return metodoView
