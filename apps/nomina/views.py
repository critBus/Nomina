import json
from typing import List

from django.contrib.auth import logout

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_reportbroD.utils import export_report_by_name

from .models import *
from .utils.utils_reportes_d import generar_reporte_sbm
