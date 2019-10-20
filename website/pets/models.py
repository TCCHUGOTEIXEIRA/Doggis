from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class Produto(models.Model):
    responsavel = models.ForeignKey(User, related_name='user_produto', on_delete=models.CASCADE)
    nome = models.CharField(max_length=256)
    fabricante = models.CharField(max_length=256)
    info = models.CharField(max_length=512, blank=True)
    registrado_em = models.DateTimeField(default=timezone.now)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

class FluxoDeEstoque(models.Model):
    responsavel = models.ForeignKey(User, related_name='user_fluxo_de_estoque', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto,related_name='produto', on_delete=models.CASCADE)
    ocorrido_em = models.DateTimeField(default=timezone.now)
    quantidade_anterior = models.PositiveIntegerField()
    quantidade_posterior = models.PositiveIntegerField()

    def __str__(self):
        return str(self.produto) + ' : @ ' + str(self.ocorrido_em) + ' | ' + str(self.quantidade_anterior) + ' -> '+ str(self.quantidade_posterior)

    def isStocking(self):
        output = self.quantidade_posterior > self.quantidade_anterior
        return output

class Servico(models.Model):
    responsavel = models.ForeignKey(User, related_name='user_servico', on_delete=models.CASCADE)
    nome = models.CharField(max_length=256)
    info = models.CharField(max_length=512, blank=True)
    criado_em = models.DateTimeField(default=timezone.now)
    tempo_estimado = models.PositiveIntegerField()
    produtos_utilizados =  models.ManyToManyField(Produto, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return self.nome

    def prestados(self):
        num = ServicoRegistro.objects.filter(servico=self).count()
        return num

class ServicoRegistro(models.Model):
    responsavel = models.ForeignKey(User, related_name='user_servico_prestado', on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, related_name='servico_prestado', on_delete=models.CASCADE)
    prestado_em = models.DateTimeField(default=timezone.now)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return  self.servico.nome + ' @ ' + str(self.prestado_em)

class TrocaDePreco(models.Model):
    responsavel = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico,related_name='servico', on_delete=models.CASCADE)
    alterado_em = models.DateTimeField(default=timezone.now)
    antigo_preco = models.DecimalField(max_digits=10, decimal_places=2)
    novo_preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return  self.servico.nome+' : R$ ' + str(self.antigo_preco) + ' -> R$ '+ str(self.novo_preco)


class Notificacao(models.Model):
    responsavel = models.ForeignKey(User, related_name='user_notificacao', on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, related_name='notificacao_servico', on_delete=models.CASCADE)
    profissionais = models.ManyToManyField(User)
    horario = models.DateTimeField(default=timezone.now)
    nome_do_cliente = models.CharField(max_length=256)
    email_do_cliente = models.EmailField()

    def __str__(self):
        return  self.servico.nome + ' @ ' + str(self.horario)
