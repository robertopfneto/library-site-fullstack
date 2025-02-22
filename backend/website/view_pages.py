from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.contrib.auth import  authenticate, login


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Leitura, Livro, Trofeu, User


def home_page(request):
    print(f'Usuário autenticado: {request.user}') 
    return render(request, '../templates/home_page.html', {'user': request.user})

@method_decorator(csrf_exempt, name='dispatch')
class LoginUser(View):

    def get(self, request):
        return render(request, '../templates/login_page.html')
        
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Isso já define automaticamente o backend correto
            request.session.save()
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos!")
            return render(request, '../templates/login_page.html')
        

def lista_livros(request):
    livros = Livro.objects.all()
    return render(request, 'book_list_page.html', {
        'livros': livros
    })

def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    leitura, created = Leitura.objects.get_or_create(
        usuario=request.user,
        livro=livro
    )

    if request.method == 'POST':
        # Alternar status de conclusão
        novo_status = not leitura.concluido
        leitura.concluido = novo_status
        leitura.save()

        # Calcular pontos apenas se marcado como lido
        if novo_status:
            pontos_base = 1
            pontos_extra = livro.paginas // 100
            total_pontos = pontos_base + pontos_extra
            
            # Atualizar pontos do usuário
            request.user.pontos += total_pontos
            request.user.save()
            
            # Sistema de troféus por categoria
            if livro.categoria:
                # Contar livros concluídos na mesma categoria
                total_na_categoria = Leitura.objects.filter(
                    usuario=request.user,
                    livro__categoria=livro.categoria,
                    concluido=True
                ).count()

                # Verificar conquista a cada 5 livros
                if total_na_categoria % 5 == 0 and total_na_categoria >= 5:
                    nome_trofeu = f"Leitor de {livro.categoria.nome}"
                    trofeu, created = Trofeu.objects.get_or_create(
                        nome=nome_trofeu,
                        defaults={
                            'descricao': f"Conquistado por ler {total_na_categoria} livros de {livro.categoria.nome}",
                            'categoria': livro.categoria
                        }
                    )
                    
                    # Adicionar troféu ao usuário se não tiver
                    if not request.user.trofeus.filter(id=trofeu.id).exists():
                        request.user.trofeus.add(trofeu)
                        messages.success(request, 
                            f"🏆 Novo troféu desbloqueado: {trofeu.nome}!",
                            extra_tags='book_detail'
                        )

            messages.success(request, 
                f"✓ Livro marcado como lido! +{total_pontos} pontos ganhos!",
                extra_tags='book_detail'
            )
        else:
            messages.info(request, 
                "✓ Status de leitura removido",
                extra_tags='book_detail'
            )

        return redirect('book-detail', id=livro.id)

    context = {
        'livro': livro,
        'leitura': leitura,
        'user': request.user
    }
    return render(request, '../templates/book_specific_page.html', context)

def perfil_usuario(request):
    usuario = request.user
    trofeus = usuario.trofeus.all()
    
    posicao = User.objects.filter(pontos__gt=usuario.pontos).count() + 1
    
    context = {
        'usuario': usuario,
        'trofeus': trofeus,
        'posicao': posicao,
        'total_usuarios': User.objects.count()
    }
    return render(request, '../templates/perfil.html', context)

def ranking(request):
    usuarios = User.objects.order_by('-pontos')
    return render(request, '../templates/ranking.html', {'usuarios': usuarios})