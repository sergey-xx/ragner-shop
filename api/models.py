import secrets

from django.db import models

from users.models import TgUser


class APIKey(models.Model):
    user = models.OneToOneField(
        TgUser, on_delete=models.CASCADE, related_name="api_key"
    )
    key = models.CharField(max_length=128, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return secrets.token_hex(32)

    def __str__(self):
        return f"API Key for {self.user.tg_id}"

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
