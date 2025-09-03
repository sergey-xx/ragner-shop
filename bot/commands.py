from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Вернутся в начало'
        ),
        # BotCommand(
        #     command='menu',
        #     description='Вернутся в главное меню'
        # ),
        # BotCommand(
        #     command='admin',
        #     description='Зайти в админ-панель'
        # )
    ]
    await bot.set_my_commands(commands)
