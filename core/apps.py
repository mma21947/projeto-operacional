from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Executado quando o app estiver pronto
        # Aqui podemos desregistrar modelos após todos os apps terem sido carregados
        import django.contrib.admin as admin
        
        # Lista de todos os modelos que não devem aparecer no admin
        apps_para_remover = ['escolas', 'pedidos', 'produtos', 'core']
        
        # Desregistrar todos os modelos dos apps na lista
        for model, model_admin in list(admin.site._registry.items()):
            app_label = model._meta.app_label
            if app_label in apps_para_remover:
                try:
                    admin.site.unregister(model)
                except admin.sites.NotRegistered:
                    pass
