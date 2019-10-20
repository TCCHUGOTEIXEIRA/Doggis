from django.urls import path, re_path
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views as pets_views

urlpatterns = [
    path('produtos/', pets_views.ProdutosView.as_view(), name='produtos'),
    path('produtos/<int:produto_id>/', pets_views.ProdutoView.as_view(), name='produto'),
    path('produtos/novo-produto/', pets_views.ProdutoNovo.as_view(), name='novo_produto'),
    path('produtos/<int:produto_id>/editar/', pets_views.ProdutoEditar.as_view(), name='editar_produto'),
    path('produtos/<int:produto_id>/deletar/', pets_views.ProdutoDeletar.as_view(), name='deletar_produto'),
    path('servicos/', pets_views.ServicosView.as_view(), name='servicos'),
    path('servicos/<int:servico_id>/', pets_views.ServicoView.as_view(), name='servico'),
    path('servicos/novo-servico/', pets_views.ServicoNovo.as_view(), name='novo_servico'),
    path('servicos/<int:servico_id>/editar/', pets_views.ServicoEditar.as_view(), name='editar_servico'),
    path('servicos/<int:servico_id>/deletar/', pets_views.ServicoDeletar.as_view(), name='deletar_servico'),
    path('servicos/<int:servico_id>/registrar/', pets_views.ServicoRegistrar.as_view(), name='registrar_servico'),
    path('servicos/<int:servico_id>/historico-de-precos/', pets_views.ServicoPrecos.as_view(), name='precos_servico'),
    path('servicos/<int:servico_id>/historico-de-prestacao/', pets_views.ServicoPrestados.as_view(), name='prestacoes_servico'),
    path('estoque/', pets_views.EstoqueView.as_view(), name='estoque'),
    path('estoque/movimentacoes', pets_views.MovimentacoesView.as_view(), name='movimentacoes'),
    path('estoque/entrada', pets_views.EstoqueEntrada.as_view(), name='estoque_entrada'),
    path('estoque/entrada/<int:produto_id>/', pets_views.EntradaProduto.as_view(), name='entrada_produto'),
    path('estoque/saida', pets_views.EstoqueSaida.as_view(), name='estoque_saida'),
    path('estoque/saida/<int:produto_id>/', pets_views.SaidaProduto.as_view(), name='saida_produto'),
    path('notificacao/', pets_views.NotificacaoView.as_view(), name='notificacao'),
    path('notificacao/nova/', pets_views.NotificacaoNovaView.as_view(), name='notificacao_nova'),
    path('notificacao/lista/', pets_views.NotificacaoListaView.as_view(), name='notificacao_lista'),    
]
