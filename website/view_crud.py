from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Categoria, Leitura, Livro, TrofeuConfig, User, Conquista
from .serializers import CategoriaSerializer, LeituraSerializer, LivroSerializer, TrofeuConfigSerializer, UserSerializer, ConquistaSerializer   

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
def categoriaAPI(request, id=0):
    if request.method == 'GET':
        if id > 0:
            try:
                categoria = Categoria.objects.get(id=id)
                serializer = CategoriaSerializer(categoria)
                return Response(serializer.data)
            except Categoria.DoesNotExist:
                return Response(
                    {"detail": "Categoria não encontrada"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            categorias = Categoria.objects.all()
            serializer = CategoriaSerializer(categorias, many=True)
            return Response(serializer.data)
    
    # Operação POST (create)
    elif request.method == 'POST':
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Categoria criada com sucesso", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": "Dados inválidos", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Operação PUT (update)
    elif request.method == 'PUT':
        try:
            categoria = Categoria.objects.get(id=id)
        except Categoria.DoesNotExist:
            return Response(
                {"detail": "Categoria não encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Categoria atualizada com sucesso", "data": serializer.data}
            )
        return Response(
            {"detail": "Dados inválidos", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Operação DELETE
    elif request.method == 'DELETE':
        try:
            categoria = Categoria.objects.get(id=id)
        except Categoria.DoesNotExist:
            return Response(
                {"detail": "Categoria não encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        categoria.delete()
        return Response(
            {"detail": "Categoria excluída com sucesso"},
            status=status.HTTP_204_NO_CONTENT
        )
    
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

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def conquistaAPI(request, id=0):
    try:
        if request.method == 'GET':
            if id > 0:
                conquista = Conquista.objects.get(id=id)
                serializer = ConquistaSerializer(conquista)
                return Response(serializer.data)
            else:
                conquistas = Conquista.objects.all().order_by('-data_conquista')
                serializer = ConquistaSerializer(conquistas, many=True)
                return Response({
                    'count': conquistas.count(),
                    'results': serializer.data
                })
        
        elif request.method == 'POST':
            serializer = ConquistaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            conquista = Conquista.objects.get(id=id)
            serializer = ConquistaSerializer(conquista, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'data': serializer.data
                })
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            conquista = Conquista.objects.get(id=id)
            conquista.delete()
            return Response({
                'status': 'success',
                'message': 'Conquista excluída'
            }, status=status.HTTP_204_NO_CONTENT)

    except Conquista.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Conquista não encontrada'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def trofeuConfigAPI(request, id=0):
    try:
        if request.method == 'GET':
            if id > 0:
                config = TrofeuConfig.objects.get(id=id)
                serializer = TrofeuConfigSerializer(config)
                return Response(serializer.data)
            else:
                configs = TrofeuConfig.objects.all().select_related('categoria')
                serializer = TrofeuConfigSerializer(configs, many=True)
                return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = TrofeuConfigSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            config = TrofeuConfig.objects.get(id=id)
            serializer = TrofeuConfigSerializer(config, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'data': serializer.data
                })
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            config = TrofeuConfig.objects.get(id=id)
            config.delete()
            return Response({
                'status': 'success',
                'message': 'Configuração de troféu excluída'
            }, status=status.HTTP_204_NO_CONTENT)

    except TrofeuConfig.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Configuração não encontrada'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)