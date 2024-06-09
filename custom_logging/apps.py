try:
    from django.apps import AppConfig
except ImportError:
    raise ImportError("Django is required to use this module")


class CustomLoggingConfig(AppConfig):
    name = "custom_logging"
    verbose_name = "Custom Logging"

    def ready(self):
        from . import signals  # noqa
