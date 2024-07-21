from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='начать с начала'),
        BotCommand(command='exchange', description='обмен деньги'),
        BotCommand(command='rates', description='соответствующие курсы валют')
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
