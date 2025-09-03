from backend.celery import app
from .utils import update_smileone_items


@app.task()
def update_smileone_items_task():
    """Фоново обновляет позиции SmileOne."""
    update_smileone_items()
