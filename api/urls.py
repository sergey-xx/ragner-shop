from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, PaymentViewSet, ProductViewSet, ProfileView

router = DefaultRouter()
router.register(r"products/pubg_uc", ProductViewSet, basename="pubg_uc_products")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("me/", ProfileView.as_view(), name="me"),
    path("", include(router.urls)),
]
