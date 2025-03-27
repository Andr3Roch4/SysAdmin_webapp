from django.contrib import admin
from .models import Produto, Fornecedor, Distribuidor, Transportador

# Register your models here.

admin.site.register(Produto)
admin.site.register(Fornecedor)
admin.site.register(Distribuidor)
admin.site.register(Transportador)