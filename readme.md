# EU JA LI! - Plataforma de Leitura e Conquistas 

- Este projeto é uma plataforma web para gestão de leituras, conquistas e rankings. Desenvolvido com Django e Django REST Framework, permite aos usuários registrar livros lidos, ganhar pontos e troféus por categorias, além de competir em rankings.


## Funcionalidades Principais
- 📚 Registro de livros por categoria
- 🏆 Sistema de conquistas baseado em leituras
- 🎯 Pontuação proporcional às páginas lidas
- 📊 Ranking de usuários por pontos
- 🔐 Autenticação de usuário
- 📈 Dashboard de perfil com conquistas

## Como Usar
1. **Pré-requisitos**:
   ```bash
   Python 3.8+
   Django 5.1
   Django REST Framework

## Instalação
 ```
    pip install django djangorestframework 
    python manage.py migrate
 ```

 ## Setup Inicial

 -  Acesse a pasta 'backend'
 ```
    cd backend
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
 ```
