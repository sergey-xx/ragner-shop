from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = 'Telegram users'

    def ready(self) -> None:
        from backend import config  # NOQA
        return super().ready()
