from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from codes.views import (
    import_codes_view,
    import_giftcards_view,
    import_stockblecode_view,
)
from payments.views import webhook_fars

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path(
        "api/v1/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("liveconfigs/", include("liveconfigs.urls"), name="liveconfigs"),
    path("import/uccodes/", import_codes_view, name="import_codes"),
    path("import/giftcards/", import_giftcards_view, name="import_giftcards"),
    path("import/stockblecode/", import_stockblecode_view, name="import_stockblecode"),
    path("webhook/fars/", webhook_fars, name="webhook_fars"),
]
