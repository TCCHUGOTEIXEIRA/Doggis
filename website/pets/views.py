from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views import View

from background_task import background
import datetime

from .sendemail import sendNotification
from .models import Servico, TrocaDePreco, Produto, ServicoRegistro, FluxoDeEstoque, Notificacao
from .forms import ProdutoForm, ProdutoDeleteForm, ServicoForm, ServicoDeleteForm, ServicoRegistrarGetForm, ServicoRegistrarPostForm, FluxoForm, NotificacaoForm


## USER PASSES TEST
# -----------------------------------------------------------------------------

def user_is_admin(user):
    return user.profile.isAdmin()

def user_is_not_client(user):
    return (not user.profile.isClient())


# PRODUTOS VIEWS
# -----------------------------------------------------------------------------

class ProdutosView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        produtos = Produto.objects.all()
        return render(request, 'produtos/index.html', {'produtos': produtos})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")

class ProdutoView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        produto_id = self.kwargs['produto_id']
        produto = Produto.objects.filter(id=produto_id).first()
        return render(request, 'produtos/view.html', {'produto': produto})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")

class ProdutoNovo(View):
    template_name = 'produtos/new.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def get(self, request, *args, **kwargs):
        form = ProdutoForm()
        return render(request, self.template_name, {'form':form})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def post(self, request, *args, **kwargs):
        form = ProdutoForm(request.POST)

        if form.is_valid():
            produto_form = form.save(commit=False)
            produto_form.responsavel = request.user
            form.save()
            return redirect('produtos')

        return render(request, self.template_name, {'form':form})

class ProdutoEditar(View):
    template_name = 'produtos/edit.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def get(self, request, *args, **kwargs):
        produto_id = self.kwargs['produto_id']
        produto = Produto.objects.filter(id=produto_id).first()

        form = ProdutoForm(instance=produto)
        return render(request, self.template_name, {'form':form, 'produto':produto})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def post(self, request, *args, **kwargs):
        produto_id = self.kwargs['produto_id']
        produto = Produto.objects.filter(id=produto_id).first()
        form = ProdutoForm(request.POST, instance=produto)

        if form.is_valid():
            form.save()
            return redirect('produto', produto_id=produto.id)

        return render(request, self.template_name, {'form':form})


class ProdutoDeletar(View):
    template_name = 'produtos/delete.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def get(self, request, *args, **kwargs):
        produto_id = self.kwargs['produto_id']
        produto = Produto.objects.filter(id=produto_id).first()
        form = ProdutoDeleteForm(instance=produto)

        return render(request, self.template_name, {'form':form, 'produto':produto})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def post(self, request, *args, **kwargs):
        produto_id = self.kwargs['produto_id']
        produto = Produto.objects.filter(id=produto_id).first()
        form = ProdutoDeleteForm(request.POST, instance=produto)

        if form.is_valid():
            produto.delete()
            return redirect('produtos')

        return render(request, self.template_name, {'form':form, 'produto':produto})


# SERVICOS VIEWS
# -----------------------------------------------------------------------------

class ServicosView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        servicos = Servico.objects.all()
        return render(request, 'servicos/index.html', {'servicos': servicos})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")

class ServicoView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        servico_id = self.kwargs['servico_id']
        servico = Servico.objects.filter(id=servico_id).first()
        return render(request, 'servicos/view.html', {'servico': servico})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")

class ServicoNovo(View):
    template_name = 'servicos/new.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def get(self, request, *args, **kwargs):
        form = ServicoForm()
        return render(request, self.template_name, {'form':form})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def post(self, request, *args, **kwargs):
        form = ServicoForm(request.POST)

        if form.is_valid():
            servico_form = form.save(commit=False)
            servico_form.responsavel = request.user
            form.save()
            return redirect('servicos')

        return render(request, self.template_name, {'form':form})

class ServicoEditar(View):
    template_name = 'servicos/edit.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def get(self, request, *args, **kwargs):
        servico_id = self.kwargs['servico_id']
        servico = Servico.objects.filter(id=servico_id).first()

        form = ServicoForm(instance=servico)
        return render(request, self.template_name, {'form':form, 'servico':servico})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def post(self, request, *args, **kwargs):
        servico_id = self.kwargs['servico_id']
        servico = Servico.objects.filter(id=servico_id).first()
        preco_antes = servico.preco

        form = ServicoForm(request.POST, instance=servico)

        if form.is_valid():
            preco_depois = form.cleaned_data['preco']
            if preco_antes != preco_depois:
                troca_de_preco = TrocaDePreco(responsavel=request.user, servico=servico, antigo_preco=preco_antes, novo_preco=preco_depois)
                troca_de_preco.save()

            form.save()
            return redirect('servico', servico_id=servico.id)

        return render(request, self.template_name, {'form':form})


class ServicoDeletar(View):
    template_name = 'servicos/delete.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def get(self, request, *args, **kwargs):
        servico_id = self.kwargs['servico_id']
        servico = Servico.objects.filter(id=servico_id).first()
        form = ServicoDeleteForm(instance=servico)

        return render(request, self.template_name, {'form':form, 'servico':servico})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def post(self, request, *args, **kwargs):
        servico_id = self.kwargs['servico_id']
        servico = Servico.objects.filter(id=servico_id).first()
        form = ServicoDeleteForm(request.POST, instance=servico)

        if form.is_valid():
            servico.delete()
            return redirect('servicos')

        return render(request, self.template_name, {'form':form, 'servico':servico})

class ServicoPrecos(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        servico_id = self.kwargs['servico_id']
        servico = Servico.objects.filter(id=servico_id).first()
        precos = TrocaDePreco.objects.filter(servico=servico).order_by('-alterado_em')
        return render(request, 'servicos/precos.html', {'servico': servico, 'precos':precos})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")

class ServicoPrestados(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        servico_id = self.kwargs['servico_id']
        servico = Servico.objects.filter(id=servico_id).first()
        registros = ServicoRegistro.objects.filter(servico=servico).order_by('-prestado_em')
        return render(request, 'servicos/hist.html', {'servico': servico, 'registros':registros})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")


class ServicoRegistrar(View):
    template_name = 'servicos/reg.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        servico_id = self.kwargs['servico_id']
        servico = Servico.objects.filter(id=servico_id).first()

        form = ServicoRegistrarGetForm(responsavel=request.user, servico=servico)

        return render(request, self.template_name, {'form':form, 'servico':servico})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def post(self, request, *args, **kwargs):
        servico_id = self.kwargs['servico_id']
        servico = Servico.objects.filter(id=servico_id).first()
        preco = servico.preco
        form = ServicoRegistrarPostForm(request.POST)

        if form.is_valid():
            servico_form = form.save(commit=False)
            servico_form.servico = servico
            servico_form.preco = preco
            form.save()
            return redirect('servicos')

        return render(request, self.template_name, {'form':form, 'servico':servico})



# ESTOQUE VIEWS
# -----------------------------------------------------------------------------

class EstoqueView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        fluxos = FluxoDeEstoque.objects.all().order_by('-ocorrido_em')[0:5]
        return render(request, 'estoque/index.html', {'fluxos':fluxos})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")

class MovimentacoesView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        fluxos = FluxoDeEstoque.objects.all().order_by('-ocorrido_em')
        return render(request, 'estoque/movimentacoes.html', {'fluxos':fluxos})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")

class EstoqueEntrada(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        produtos = Produto.objects.all()
        return render(request, 'estoque/entrada.html', {'produtos':produtos})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")

class EntradaProduto(View):
    template_name = 'estoque/entrada_produto.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def get(self, request, *args, **kwargs):
        produto_id = self.kwargs['produto_id']
        produto =  Produto.objects.filter(id=produto_id).first()
        form = FluxoForm()
        return render(request, self.template_name, {'form':form, 'produto':produto})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def post(self, request, *args, **kwargs):
        form = FluxoForm(request.POST)
        produto_id = self.kwargs['produto_id']
        produto =  Produto.objects.filter(id=produto_id).first()
        quantidade_anterior = produto.quantidade
        quantidade = int(request.POST.get('quantidade'))

        if form.is_valid():
            entrada_form = form.save(commit=False)

            entrada_form.responsavel = request.user
            entrada_form.produto = produto
            entrada_form.quantidade_anterior = quantidade_anterior
            entrada_form.quantidade_posterior = quantidade_anterior + quantidade

            produto.quantidade = quantidade_anterior + quantidade
            produto.save()

            form.save()
            return redirect('estoque')

        return render(request, self.template_name, {'form':form})

class EstoqueSaida(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        produtos = Produto.objects.all()
        return render(request, 'estoque/saida.html', {'produtos':produtos})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")


class SaidaProduto(View):
    template_name = 'estoque/saida_produto.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def get(self, request, *args, **kwargs):
        produto_id = self.kwargs['produto_id']
        produto =  Produto.objects.filter(id=produto_id).first()
        form = FluxoForm()
        return render(request, self.template_name, {'form':form, 'produto':produto})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_admin))
    def post(self, request, *args, **kwargs):
        form = FluxoForm(request.POST)
        produto_id = self.kwargs['produto_id']
        produto =  Produto.objects.filter(id=produto_id).first()
        quantidade_anterior = produto.quantidade
        quantidade = int(request.POST.get('quantidade'))

        if form.is_valid():
            entrada_form = form.save(commit=False)

            entrada_form.responsavel = request.user
            entrada_form.produto = produto
            entrada_form.quantidade_anterior = quantidade_anterior
            entrada_form.quantidade_posterior = quantidade_anterior - quantidade

            produto.quantidade = quantidade_anterior - quantidade
            produto.save()

            form.save()
            return redirect('estoque')

        return render(request, self.template_name, {'form':form})


# NOTIFICACAO VIEWS
# -----------------------------------------------------------------------------

class NotificacaoView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        notificacoes = Notificacao.objects.all().order_by('-horario')[0:3]
        return render(request, 'notificacao/index.html', {'notificacoes':notificacoes})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")

@background(schedule=15)
def notify_user(nome, user_email, horario, servico):
    print('Scheduling e-mail . . . ')
    sendNotification(nome, user_email, horario, servico)


class NotificacaoNovaView(View):
    template_name = 'notificacao/new.html'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        form = NotificacaoForm()
        return render(request, self.template_name, {'form':form})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def post(self, request, *args, **kwargs):
        form = NotificacaoForm(request.POST)

        if form.is_valid():

            horario_raw = str(form.cleaned_data['horario'])[:-6]
            horario_datetime = datetime.datetime.strptime(horario_raw, '%Y-%m-%d %H:%M:%S')
            horario = horario_datetime.strftime("%Hh%M do dia %d/%m")
            horario_email = horario_datetime - datetime.timedelta(hours=4)
            horario_delta = horario_email - datetime.datetime.now()
            schedule_secs = int(horario_delta.total_seconds())
            print(schedule_secs)

            if schedule_secs > 14400:
                schedule_secs = int(3)

            nome = str(form.cleaned_data['nome_do_cliente'])
            email = str(form.cleaned_data['email_do_cliente'])
            servico = str(form.cleaned_data['servico'])

            notificacao_form = form.save(commit=False)
            notificacao_form.responsavel = request.user
            form.save()

            # email task
            notify_user(nome, email, horario, servico, schedule=schedule_secs)

            return redirect('notificacao')

        return render(request, self.template_name, {'form':form})


class NotificacaoListaView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(user_is_not_client))
    def get(self, request, *args, **kwargs):
        notificacoes = Notificacao.objects.all().order_by('-horario')
        return render(request, 'notificacao/list.html', {'notificacoes':notificacoes})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotFound("404")
