from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        # import signals so they are registered
        # Keep import inside ready() to avoid side effects at import time.
        try:
            import properties.signals  # noqa: F401
        except Exception:
            # It's good to fail loudly during development, but avoid crashing imports in weird environments.
            # We re-raise so issues surface while developing; remove the try/except if you want strict failures.
            raise
