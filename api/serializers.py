from decimal import Decimal

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from items.models import Item, PUBGUCItem
from orders.models import Order, TopUp
from users.models import TgUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = ("tg_id", "username", "first_name", "balance")


class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()

    class Meta:
        model = PUBGUCItem
        fields = ("id", "title", "price", "amount", "stock")

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_stock(self, obj: Item):
        return obj.get_stock_amount()


class OrderSerializer(serializers.ModelSerializer):
    item_title = serializers.CharField(source="item.title", read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "item_title",
            "quantity",
            "price",
            "status",
            "pubg_id",
            "created_at",
        )


class CreateOrderSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    pubg_id = serializers.CharField(max_length=50, required=False, allow_null=True)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUp
        fields = ("id", "amount", "to_pay", "is_paid", "created_at")


class CreatePaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("1.00")
    )
