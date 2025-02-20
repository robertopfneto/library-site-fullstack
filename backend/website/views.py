from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.parsers import JSONParser

from .models import Leitura, Livro, Trofeu, User
from .serializers import LeituraSerializer, LivroSerializer, TrofeuSerializer, UserSerializer

#User: nome, senha, pontos, trofeus
#Trofeu: nome, desc
#Livro: titulo, autor, paginas,imagem
#Leitura: Usuario, Livro, data

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def userAPI(request, id=0):
    if request.method == 'GET':
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Cadastro realizado com sucesso", status=status.HTTP_201_CREATED)
        return Response("Falha ao adicionar usuário", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response("Usuário não encontrado", status=status.HTTP_404_NOT_FOUND)
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Usuário atualizado com sucesso")
        return Response("Falha ao atualizar usuário", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response("Usuário não encontrado", status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response("Usuário deletado com sucesso")
    
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def livroAPI(request, id=0):
    if request.method == 'GET':
        livros = Livro.objects.all()
        livro_serializer = LivroSerializer(livros, many=True)
        return Response(livro_serializer.data)
    elif request.method == 'POST':
        livro_serializer = LivroSerializer(data=request.data)
        if livro_serializer.is_valid():
            livro_serializer.save()
            return Response("Livro cadastrado com sucesso", status=status.HTTP_201_CREATED)
        return Response("Falha ao adicionar livro", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            livro = Livro.objects.get(id=id)
        except Livro.DoesNotExist:
            return Response("Livro não encontrado", status=status.HTTP_404_NOT_FOUND)
        livro_serializer = LivroSerializer(livro, data=request.data)
        if livro_serializer.is_valid():
            livro_serializer.save()
            return Response("Livro atualizado com sucesso")
        return Response("Falha ao atualizar livro", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            livro = Livro.objects.get(id=id)
        except Livro.DoesNotExist:
            return Response("Livro não encontrado", status=status.HTTP_404_NOT_FOUND)
        livro.delete()
        return Response("Livro deletado com sucesso")

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def trofeuAPI(request, id=0):
    if request.method == 'GET':
        trofeus = Trofeu.objects.all()
        trofeu_serializer = TrofeuSerializer(trofeus, many=True)
        return Response(trofeu_serializer.data)
    elif request.method == 'POST':
        trofeu_serializer = TrofeuSerializer(data=request.data)
        if trofeu_serializer.is_valid():
            trofeu_serializer.save()
            return Response("Troféu cadastrado com sucesso", status=status.HTTP_201_CREATED)
        return Response("Falha ao adicionar troféu", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            trofeu = Trofeu.objects.get(id=id)
        except Trofeu.DoesNotExist:
            return Response("Troféu não encontrado", status=status.HTTP_404_NOT_FOUND)
        trofeu_serializer = TrofeuSerializer(trofeu, data=request.data)
        if trofeu_serializer.is_valid():
            trofeu_serializer.save()
            return Response("Troféu atualizado com sucesso")
        return Response("Falha ao atualizar troféu", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            trofeu = Trofeu.objects.get(id=id)
        except Trofeu.DoesNotExist:
            return Response("Troféu não encontrado", status=status.HTTP_404_NOT_FOUND)
        trofeu.delete()
        return Response("Troféu deletado com sucesso")

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def leituraAPI(request, id=0):
    if request.method == 'GET':
        leituras = Leitura.objects.all()
        leitura_serializer = LeituraSerializer(leituras, many=True)
        return Response(leitura_serializer.data)
    elif request.method == 'POST':
        leitura_serializer = LeituraSerializer(data=request.data)
        if leitura_serializer.is_valid():
            leitura_serializer.save()
            return Response("Leitura cadastrada com sucesso", status=status.HTTP_201_CREATED)
        return Response("Falha ao adicionar leitura", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            leitura = Leitura.objects.get(id=id)
        except Leitura.DoesNotExist:
            return Response("Leitura não encontrada", status=status.HTTP_404_NOT_FOUND)
        leitura_serializer = LeituraSerializer(leitura, data=request.data)
        if leitura_serializer.is_valid():
            leitura_serializer.save()
            return Response("Leitura atualizada com sucesso")
        return Response("Falha ao atualizar leitura", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            leitura = Leitura.objects.get(id=id)
        except Leitura.DoesNotExist:
            return Response("Leitura não encontrada", status=status.HTTP_404_NOT_FOUND)
        leitura.delete()
        return Response("Leitura deletada com sucesso")