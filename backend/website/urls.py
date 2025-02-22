from django.urls import include, path
from rest_framework import routers

from .view_pages import home_page, LoginUser as login_user, perfil_usuario, ranking
from.view_pages import lista_livros, detalhe_livro
from .view_crud import userAPI, livroAPI, leituraAPI, trofeuAPI



router = routers.DefaultRouter()

urlpatterns = [
    #path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    path('home/', home_page, name='home'),
    path('livros/', lista_livros, name="book-list"),
    path('livros/<int:id>/', detalhe_livro, name="book-detail"),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
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
    path('livro/imagem/<int:id>/', livroAPI, name='livro-imagem'), #upload de imagem

    # Rotas para Trofeu
    path('trofeu/', trofeuAPI, name='trofeu-list-create'),
    path('trofeu/<int:id>/', trofeuAPI, name='trofeu-detail'),

    # Rotas para Leitura
    path('leitura/', leituraAPI, name='leitura-list-create'),
    path('leitura/<int:id>/', leituraAPI, name='leitura-detail'),

]