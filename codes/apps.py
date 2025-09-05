from django.apps import AppConfig
from django.db.models.signals import post_migrate


def populate_activator_priorities(sender, **kwargs):
    from .models import Activator, ActivatorPriority

    for name, label in Activator.choices:
        ActivatorPriority.objects.get_or_create(name=name)
    print("Activator priorities populated.")


class CodesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codes"

    def ready(self) -> None:
        import codes.signals  # NOQA

        post_migrate.connect(populate_activator_priorities, sender=self)
        return super().ready()
