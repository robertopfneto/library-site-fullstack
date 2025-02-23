from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    pontos = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class TrofeuConfig(models.Model):
    categoria = models.OneToOneField(
        Categoria, 
        on_delete=models.CASCADE,
        related_name='config_trofeu'
    )
    livros_necessarios = models.PositiveIntegerField(default=5)
    pontos_recompensa = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"Config: {self.categoria.nome}"

class Conquista(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conquistas')
    trofeu_config = models.ForeignKey(TrofeuConfig, on_delete=models.CASCADE)
    data_conquista = models.DateTimeField(auto_now_add=True)
    nivel = models.PositiveIntegerField(default=1)  # Novo campo para rastrear o nível

    def __str__(self):
        return f"{self.usuario} - {self.trofeu_config.categoria.nome} (Nível {self.nivel})"

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    paginas = models.IntegerField()
    imagem = models.ImageField(upload_to='livros/', blank=True, null=True)
    sinopse = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
    )
    data_cadastro = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Leitura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    concluido = models.BooleanField(default=False)
    data_leitura = models.DateTimeField(auto_now_add=True)  # Campo adicionado

    class Meta:
        unique_together = ['usuario', 'livro']

    def __str__(self):
        return f"{self.usuario} - {self.livro.titulo}"