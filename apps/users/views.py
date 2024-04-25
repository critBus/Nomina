import traceback

import requests
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User

from ..base.views import *
from .serializers import *
