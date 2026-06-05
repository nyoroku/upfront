from django.apps import AppConfig


class LanesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.lanes'
    verbose_name = 'Lane Tracker'

    def ready(self):
        import apps.lanes.signals  # noqa: F401
