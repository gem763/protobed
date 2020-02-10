from django.apps import AppConfig


class FlorenceConfig(AppConfig):
    name = 'florence'

    def ready(self):
        import florence.signals
