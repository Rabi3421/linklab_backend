from django.apps import AppConfig


class LinklabAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'linklab_app'

    def ready(self):
        # Import signals when the app is loaded
        import linklab_app.signals


