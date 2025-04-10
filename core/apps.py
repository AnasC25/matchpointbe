from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):  # ✅ La méthode `ready` doit être à l'intérieur de `CoreConfig`
        import core.signals # Assure que les signaux sont bien importés
