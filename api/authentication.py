from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return None

        try:
            key_instance = APIKey.objects.select_related("user").get(key=api_key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API Key.")

        return (key_instance.user, None)
