from drf_spectacular.extensions import OpenApiAuthenticationExtension


class APIKeyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "api.authentication.APIKeyAuthentication"
    name = "ApiKeyAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API Key obtained from the Telegram bot.",
        }
