from django.contrib import admin
from .models import Servico, TrocaDePreco, Produto, FluxoDeEstoque

admin.site.register(Servico)
admin.site.register(TrocaDePreco)
admin.site.register(Produto)
admin.site.register(FluxoDeEstoque)
