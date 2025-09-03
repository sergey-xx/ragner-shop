from django.contrib import admin
from django.urls import include, path

from codes.views import (import_codes_view, import_giftcards_view,
                         import_stockblecode_view)

from payments.views import webhook_fars

urlpatterns = [
    path('admin/', admin.site.urls),
    path('liveconfigs/', include('liveconfigs.urls'), name='liveconfigs'),
    path('import/uccodes/', import_codes_view, name='import_codes'),
    path('import/giftcards/', import_giftcards_view, name='import_giftcards'),
    path('import/stockblecode/', import_stockblecode_view, name='import_stockblecode'),
    path('webhook/fars/', webhook_fars, name='webhook_fars'),
]
