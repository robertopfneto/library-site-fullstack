from django.urls import include, path
from rest_framework import routers

from .view_pages import home_page, LoginUser as login_user, perfil_usuario, ranking
from.view_pages import lista_livros, detalhe_livro
from .view_crud import categoriaAPI, conquistaAPI, trofeuConfigAPI, userAPI, livroAPI, leituraAPI



router = routers.DefaultRouter()

urlpatterns = [
    #path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    path('home/', home_page, name='home'),
    path('livros/', lista_livros, name="book-list"),
    path('livros/<int:id>/', detalhe_livro, name="book-detail"),
    path('perfil/', perfil_usuario, name='perfil_usuario'),  # Perfil próprio
    path('perfil/<int:id>/', perfil_usuario, name='perfil_usuario_detail'),  # Perfil de outros
    path('ranking/', ranking, name='ranking'),


    # Rotas para User
    path('user/', userAPI, name='user'),  # GET all, POST create
    path('user/<int:id>/', userAPI, name='user-detail'),  # GET, PUT, DELETE


    #Web
    path('', login_user.as_view(), name='login'),  # POST login
    path('user/logout/', userAPI, name='logout'),  # POST logout


    # Rotas para Livro
    path('livro/', livroAPI, name='livro-list-create'),
    path('livro/<int:id>/', livroAPI, name='livro-detail'),
    path('livro/imagem/<int:id>/', livroAPI, name='livro-imagem'),
     #upload de imagem

    # Rotas para Leitura
    path('leitura/', leituraAPI, name='leitura-list-create'),
    path('leitura/<int:id>/', leituraAPI, name='leitura-detail'),

    #Rotas para Categoria
    path('categoria/', categoriaAPI, name='categoria-list-create'),
    path('categoria/<int:id>/', categoriaAPI, name='categoria-detail'),

    #Rotas para Conquista
    path('conquista/', conquistaAPI, name='conquista-list-create'),
    path('conquista/<int:id>/', conquistaAPI, name='conquista-detail'),

    #Rotas para TrofeuConfig
    path('trofeuconfig/', trofeuConfigAPI, name='trofeuconfig-list-create'),
    path('trofeuconfig/<int:id>/', trofeuConfigAPI, name='trofeuconfig-detail'),
]