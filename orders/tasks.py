import logging

from backend.celery import app
from items.models import Item
from .models import Order
from .utils import process_diamond

logger = logging.getLogger(__name__)


@app.task()
def process_order_task(order_id):
    """Фоново обрабатывает заказ."""
    order = Order.objects.select_related('item',).get(id=order_id)
    if order.item.category == Item.Category.DIAMOND:
        process_diamond(order)
