from items.tasks import update_smileone_items_task


async def start_background_tasks():
    update_smileone_items_task.delay()
