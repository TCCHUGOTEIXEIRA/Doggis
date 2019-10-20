from django import forms

from .models import Servico, ServicoRegistro, TrocaDePreco, Produto, FluxoDeEstoque, Notificacao

class NotificacaoForm(forms.ModelForm):
    class Meta:
        model = Notificacao
        fields = ('servico', 'profissionais', 'horario', 'nome_do_cliente', 'email_do_cliente')

class FluxoForm(forms.ModelForm):
    class Meta:
        model = FluxoDeEstoque
        fields = ('ocorrido_em',)

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ('nome', 'fabricante', 'info', 'preco' ,'quantidade')

class ProdutoDeleteForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = []

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ('nome', 'info', 'preco' ,'tempo_estimado', 'produtos_utilizados')

class ServicoDeleteForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = []

class ServicoRegistrarGetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.responsavel = kwargs.pop('responsavel')
        self.servico = kwargs.pop('servico')

        super(ServicoRegistrarGetForm, self).__init__(*args, **kwargs)

        self.fields['responsavel'].initial =  self.responsavel

    class Meta:
        model = ServicoRegistro
        fields = ('responsavel','prestado_em')

class ServicoRegistrarPostForm(forms.ModelForm):

    class Meta:
        model = ServicoRegistro
        fields = ('responsavel','prestado_em')
