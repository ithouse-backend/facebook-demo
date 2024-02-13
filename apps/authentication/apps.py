from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"

    def ready(self):
        """
        qanchonki dasturimiz ishlashga tayyor bo'lganda
        """
        from . import signals
