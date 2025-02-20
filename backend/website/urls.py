from django.urls import include, path
from rest_framework import routers
from .views import userAPI, livroAPI, leituraAPI, trofeuAPI


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Rotas para User
    path('user/', userAPI, name='user-list-create'),  # GET all, POST create
    path('user/<int:id>/', userAPI, name='user-detail'),  # GET, PUT, DELETE

    # Rotas para Livro
    path('livro/', livroAPI, name='livro-list-create'),
    path('livro/<int:id>/', livroAPI, name='livro-detail'),

    # Rotas para Trofeu
    path('trofeu/', trofeuAPI, name='trofeu-list-create'),
    path('trofeu/<int:id>/', trofeuAPI, name='trofeu-detail'),

    # Rotas para Leitura
    path('leitura/', leituraAPI, name='leitura-list-create'),
    path('leitura/<int:id>/', leituraAPI, name='leitura-detail'),

]