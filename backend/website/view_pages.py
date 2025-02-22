from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.contrib.auth import  authenticate, login


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Conquista, Leitura, Livro, TrofeuConfig, User
from .serializers import LivroSerializer


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate
from django.db.models import Count
from django.db import models
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Categoria, Conquista, Leitura, Livro, TrofeuConfig, User
from .serializers import LivroSerializer

def home_page(request):
    return render(request, '../templates/home_page.html', {'user': request.user})

@method_decorator(csrf_exempt, name='dispatch')
class LoginUser(View):
    def get(self, request):
        return render(request, '../templates/login_page.html')
        
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, "Credenciais inválidas!")
        return render(request, '../templates/login_page.html')

def lista_livros(request):
    livros = Livro.objects.select_related('categoria').all()
    return render(request, 'book_list_page.html', {'livros': livros})

def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro.objects.select_related('categoria'), id=livro_id)
    leitura, created = Leitura.objects.get_or_create(usuario=request.user, livro=livro)

    if request.method == 'POST':
        return leitura_status(request, livro, leitura)

    context = get_livro_context(livro, leitura, request.user)
    return render(request, '../templates/book_specific_page.html', context)

def leitura_status(request, livro, leitura):
    novo_status = not leitura.concluido
    leitura.concluido = novo_status
    leitura.save()

    if novo_status:
        return marcar_como_lido(request, livro)
    return desmarcar_como_lido(request, livro)

def marcar_como_lido(request, livro):
    pontos = calcular_pontos(livro)
    request.user.pontos += pontos
    request.user.save()
    
    if livro.categoria:
        conquistas(request, request.user, livro.categoria, pontos)  # Passe request
    
    messages.success(request, 
        f"✓ Livro marcado como lido! +{pontos} pontos ganhos!",
        extra_tags='book_detail'
    )
    return redirect('book-detail', id=livro.id)

def desmarcar_como_lido(request, livro):
    pontos = calcular_pontos(livro)
    request.user.pontos = max(0, request.user.pontos - pontos)
    request.user.save()
    
    messages.info(request, 
        "✓ Status de leitura removido - Pontos retirados",
        extra_tags='book_detail'
    )
    return redirect('book-detail', id=livro.id)

def calcular_pontos(livro):
    return 1 + (livro.paginas // 100)

def conquistas(request, usuario, categoria, pontos):  # Adicione request
    try:
        config = TrofeuConfig.objects.get(categoria=categoria)
        total_lidos = Leitura.objects.filter(
            usuario=usuario,
            livro__categoria=categoria,
            concluido=True
        ).count()

        nivel_anterior = total_lidos // config.livros_necessarios
        novo_nivel = (total_lidos + 1) // config.livros_necessarios

        if novo_nivel > nivel_anterior:
            pontos_recompensa = config.pontos_recompensa * novo_nivel
            usuario.pontos += pontos_recompensa
            usuario.save()
            
            Conquista.objects.create(
                usuario=usuario,
                trofeu_config=config
            )
            messages.success(request,  # Agora request está definido
                f"🏆 Troféu conquistado! +{pontos_recompensa} pontos",
                extra_tags='book_detail'
            )
    except TrofeuConfig.DoesNotExist:
        pass

def get_livro_context(livro, leitura, user):
    conquistas = Conquista.objects.filter(
        usuario=user,
        trofeu_config__categoria=livro.categoria
    ).select_related('trofeu_config') if livro.categoria else []

    return {
        'livro': LivroSerializer(livro).data,
        'leitura': {
            'concluido': leitura.concluido,
            'data_leitura': leitura.data_leitura
        },
        'conquistas': conquistas,
        'user': {
            'username': user.username,
            'pontos': user.pontos
        }
    }

def perfil_usuario(request):
    usuario = request.user
    conquistas = Conquista.objects.filter(usuario=usuario).select_related('trofeu_config')
    
    posicao = User.objects.filter(pontos__gt=usuario.pontos).count() + 1
    
    context = {
        'usuario': usuario,
        'conquistas': conquistas,
        'posicao': posicao,
        'total_usuarios': User.objects.count()
    }
    return render(request, '../templates/perfil.html', context)

def ranking(request):
    usuarios = User.objects.annotate(
        total_lidos=Count('leitura', filter=models.Q(leitura__concluido=True))
    ).order_by('-pontos')
    
    return render(request, '../templates/ranking.html', {
        'usuarios': usuarios
    })