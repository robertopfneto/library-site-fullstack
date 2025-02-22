from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.contrib.auth import  authenticate, login


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


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
