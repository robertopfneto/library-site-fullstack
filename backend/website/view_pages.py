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
from django.db.models import Count, Q
from django.db import models


from .models import Conquista, Leitura, Livro, TrofeuConfig, User
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

def detalhe_livro(request, id):
    livro = get_object_or_404(Livro.objects.select_related('categoria'), id=id)
    leitura, created = Leitura.objects.get_or_create(
        usuario=request.user,
        livro=livro,
        defaults={'concluido': False}  # Garante valores padrão
    )
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


# Seta trofeu para o usuário
def conquistas(request, usuario, categoria, pontos):
    try:
        config = TrofeuConfig.objects.get(categoria=categoria)
        total_lidos = Leitura.objects.filter(
            usuario=usuario,
            livro__categoria=categoria,
            concluido=True
        ).count()

        # Calcular quantos níveis foram alcançados (cada 5 livros)
        niveis_conquistados = total_lidos // config.livros_necessarios
        
        # Verificar conquistas já registradas
        conquistas_existentes = Conquista.objects.filter(
            usuario=usuario,
            trofeu_config=config
        ).count()

        # Atribuir novos troféus se necessário
        if niveis_conquistados > conquistas_existentes:
            for nivel in range(conquistas_existentes + 1, niveis_conquistados + 1):
                pontos_recompensa = config.pontos_recompensa * nivel
                usuario.pontos += pontos_recompensa
                Conquista.objects.create(
                    usuario=usuario,
                    trofeu_config=config,
                    nivel=nivel
                )
                messages.success(
                    request,
                    f"🏆 Troféu conquistado: Leitor de {categoria.nome} (Nível {nivel})! +{pontos_recompensa} pontos",
                    extra_tags='book_detail'
                )
            usuario.save()
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

def perfil_usuario(request, id=None):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if id is None:
        usuario = request.user
    else:
        usuario = get_object_or_404(User, id=id)
    
    conquistas = Conquista.objects.filter(usuario=usuario).select_related('trofeu_config__categoria')
    
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
        total_lidos=Count('leitura', filter=models.Q(leitura__concluido=True)),
        total_conquistas=Count('conquistas')  # Mudar para o related_name correto
    ).order_by('-pontos')
    
    return render(request, '../templates/ranking.html', {
        'usuarios': usuarios
    })