from django.db import models

#User: nome, senha, pontos, trofeus
#Trofeu: nome, desc
#Livro: titulo, autor, paginas, imagem
#Leitura: Usuario, Livro, data


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    pontos = models.IntegerField(default=0)
    trofeus = models.ManyToManyField('Trofeu', blank=True)
    last_login = models.DateTimeField(auto_now=True)

    # Campos obrigatórios para compatibilidade com Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    # Métodos necessários para compatibilidade
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    

    
class Trofeu(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=20)
    descricao = models.CharField(max_length=100)
    data_conquista = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    paginas = models.IntegerField()
    imagem = models.ImageField(upload_to='livros/', blank=True, null=True)
    descricao = models.TextField(blank=True)
    categoria =  models.ForeignKey('Categoria', on_delete=models.CASCADE)
    data_cadastro = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Leitura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    concluido = models.BooleanField(default=False)

