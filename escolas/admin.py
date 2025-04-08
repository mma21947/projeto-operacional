from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Escola, Supervisor

class SupervisorResource(resources.ModelResource):
    class Meta:
        model = Supervisor
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'nome', 'email', 'telefone', 'ativo')

@admin.register(Supervisor)
class SupervisorAdmin(ImportExportModelAdmin):
    resource_class = SupervisorResource
    list_display = ('nome', 'email', 'telefone', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'email', 'telefone')
    list_editable = ('ativo',)

class EscolaResource(resources.ModelResource):
    class Meta:
        model = Escola
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'nome', 'codigo', 'lote', 'empresa', 'endereco', 'cep', 'cidade', 'estado', 
                  'telefone', 'email', 'supervisor', 'ativo')

@admin.register(Escola)
class EscolaAdmin(ImportExportModelAdmin):
    resource_class = EscolaResource
    list_display = ('nome', 'codigo', 'lote', 'empresa', 'cidade', 'estado', 'supervisor', 'ativo')
    list_filter = ('ativo', 'estado', 'supervisor')
    search_fields = ('nome', 'codigo', 'endereco', 'cidade')
    list_editable = ('ativo',)
    autocomplete_fields = ['supervisor']
