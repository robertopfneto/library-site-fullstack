from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import JSONParser

from .models import Leitura, Livro, Trofeu, User
from .serializers import LeituraSerializer, LivroSerializer, TrofeuSerializer, UserSerializer
# Create your views here.

@csrf_exempt
def userAPI(request, id=0):
    if request.method == 'GET':
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Cadastro Realizado com sucesso", safe=False)
        return JsonResponse("Falha em adicionar Usuário", safe=False)
    
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user = User.objects.get(id=user_data['id'])
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Usuário atualizado com sucesso", safe=False)
        return JsonResponse("Falha em atualizar Usuário", safe=False)
    
    elif request.method == 'DELETE':
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse("Usuário deletado com sucesso", safe=False)
    

@csrf_exempt
def livroAPI(request, id=0):
    if request.method == 'GET':
        livros = Livro.objects.all()
        livro_serializer = LivroSerializer(livros, many=True)
        return JsonResponse(livro_serializer.data, safe=False)
    elif request.method == 'POST':
        livro_data = JSONParser().parse(request)
        livro_serializer = LivroSerializer(data=livro_data)
        if livro_serializer.is_valid():
            livro_serializer.save()
            return JsonResponse("Cadastro Realizado com sucesso", safe=False)
        return JsonResponse("Falha em adicionar Livro", safe=False)
    
    elif request.method == 'PUT':
        livro_data = JSONParser().parse(request)
        livro = Livro.objects.get(id=livro_data['id'])
        livro_serializer = LivroSerializer(livro, data=livro_data)
        if livro_serializer.is_valid():
            livro_serializer.save()
            return JsonResponse("Livro atualizado com sucesso", safe=False)
        return JsonResponse("Falha em atualizar Livro", safe=False)
    
    elif request.method == 'DELETE':
        livro = Livro.objects.get(id=id)
        livro.delete()
        return JsonResponse("Livro deletado com sucesso", safe=False)
    
@csrf_exempt
def trofeuAPI(request, id=0):
    if request.method == 'GET':
        trofeus = Trofeu.objects.all()
        trofeu_serializer = TrofeuSerializer(trofeus, many=True)
        return JsonResponse(trofeu_serializer.data, safe=False)
    elif request.method == 'POST':
        trofeu_data = JSONParser().parse(request)
        trofeu_serializer = TrofeuSerializer(data=trofeu_data)
        if trofeu_serializer.is_valid():
            trofeu_serializer.save()
            return JsonResponse("Cadastro Realizado com sucesso", safe=False)
        return JsonResponse("Falha em adicionar Trofeu", safe=False)
    
    elif request.method == 'PUT':
        trofeu_data = JSONParser().parse(request)
        trofeu = Trofeu.objects.get(id=trofeu_data['id'])
        trofeu_serializer = TrofeuSerializer(trofeu, data=trofeu_data)
        if trofeu_serializer.is_valid():
            trofeu_serializer.save()
            return JsonResponse("Trofeu atualizado com sucesso", safe=False)
        return JsonResponse("Falha em atualizar Trofeu", safe=False)
    
    elif request.method == 'DELETE':
        trofeu = Trofeu.objects.get(id=id)
        trofeu.delete()
        return JsonResponse("Trofeu deletado com sucesso", safe=False)
    
@csrf_exempt
def leituraAPI(request, id=0):
    if request.method == 'GET':
        leituras = Leitura.objects.all()
        leitura_serializer = LeituraSerializer(leituras, many=True)
        return JsonResponse(leitura_serializer.data, safe=False)
    elif request.method == 'POST':
        leitura_data = JSONParser().parse(request)
        leitura_serializer = LeituraSerializer(data=leitura_data)
        if leitura_serializer.is_valid():
            leitura_serializer.save()
            return JsonResponse("Cadastro Realizado com sucesso", safe=False)
        return JsonResponse("Falha em adicionar Leitura ao", safe=False)
    
    elif request.method == 'PUT':
        leitura_data = JSONParser().parse(request)
        leitura = Leitura.objects.get(id=leitura_data['id'])
        leitura_serializer = LeituraSerializer(leitura, data=leitura_data)
        if leitura_serializer.is_valid():
            leitura_serializer.save()
            return JsonResponse("Leitura atualizado com sucesso", safe=False)
        return JsonResponse("Falha em atualizar Leitura", safe=False)
    
    elif request.method == 'DELETE':
        leitura = Leitura.objects.get(id=id)
        leitura.delete()
        return JsonResponse("L deletado com sucesso", safe=False)
    
