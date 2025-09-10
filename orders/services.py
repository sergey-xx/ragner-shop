import logging

from asgiref.sync import sync_to_async
from django.db import transaction

from items.models import Item
from users.models import TgUser

from .models import Order

logger = logging.getLogger(__name__)


class OrderCreationError(Exception):
    """Базовый класс для ошибок создания заказа."""

    pass


class InsufficientBalanceError(OrderCreationError):
    """Ошибка при недостаточном балансе."""

    pass


class OutOfStockError(OrderCreationError):
    """Ошибка, если товара нет в наличии."""

    pass


class ItemNotActiveError(OrderCreationError):
    """Ошибка, если товар неактивен."""

    pass


@sync_to_async
@transaction.atomic
def create_order_service(
    *,
    tg_user: TgUser,
    item: Item,
    quantity: int = 1,
    pubg_id: str | None = None,
) -> Order:
    if not item.is_active:
        raise ItemNotActiveError("This item is currently not available for purchase.")

    is_stockable = item.category in (Item.Category.CODES, Item.Category.GIFTCARD)
    if not is_stockable and quantity != 1:
        logger.warning(
            f"Attempted to buy non-stockable item #{item.id} with quantity {quantity}. "
            f"Forcing quantity to 1 for user {tg_user.tg_id}."
        )
        quantity = 1

    price = item.price * quantity
    if price > tg_user.balance:
        raise InsufficientBalanceError("You do not have enough balance.")

    stock = item.get_stock_amount()
    if stock is not None and stock < quantity:
        raise OutOfStockError(f"Not enough stock. Available: {stock}")

    locked_user = TgUser.objects.select_for_update().get(id=tg_user.id)

    order = Order.objects.create(
        tg_user=locked_user,
        item=item,
        quantity=quantity,
        data=item.to_dict(),
        price=price,
        category=item.category,
        pubg_id=pubg_id,
        balance_before=locked_user.balance,
    )

    logger.info(f"Order #{order.id} created for user {tg_user.tg_id} via service.")

    order.grab_codes()

    return order
