from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=250)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=250)
    imagem = models.ImageField(upload_to='imagens')
    preco = models.FloatField()
    descricao = models.TextField()
    quantidade_estoque = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrinho')
    produtos = models.ManyToManyField(Produto)
