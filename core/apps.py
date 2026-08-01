from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # COMMENT OUT signals during migration
        # import core.signals  # noqa

        # COMMENT OUT ML models during migration
        # try:
        #     from core.ml_models import load_models
        #     load_models()
        # except Exception:
        #     pass
        pass