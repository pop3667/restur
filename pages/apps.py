from django.apps import AppConfig
import pages

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    def ready(self):
        import pages.signals
