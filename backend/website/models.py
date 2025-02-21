from django.db import models

#User: nome, senha, pontos, trofeus
#Trofeu: nome, desc
#Livro: titulo, autor, paginas, imagem
#Leitura: Usuario, Livro, data

class User(models.Model):
    nome = models.CharField(max_length=20)
    senha = models.CharField(max_length=100)
    pontos = models.IntegerField()
    trofeus = models.ManyToManyField('Trofeu')

class Trofeu(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.CharField(max_length=100)

class Livro(models.Model):
    titulo = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    paginas = models.IntegerField()
    imagem = models.ImageField(upload_to='livro/imagens/', null=True, blank=True)

class Leitura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data = models.DateField()