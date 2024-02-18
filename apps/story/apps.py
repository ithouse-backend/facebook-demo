from django.apps import AppConfig


class StoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.story'

    def ready(self):
        from . import signals
