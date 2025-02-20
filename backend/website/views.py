from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import JSONParser

from .models import Leitura, Livro, Trofeu, User
from .serializers import LeituraSerializer, LivroSerializer, TrofeuSerializer, UserSerializer
# Create your views here.
