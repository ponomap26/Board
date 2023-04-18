from django.apps import AppConfig


class BrdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'brd'
    def ready(self):
        from . import signals