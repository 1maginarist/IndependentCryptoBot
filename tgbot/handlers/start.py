from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter


async def command_start(message: types.Message):
    await message.answer(f"Welcome, {message.from_user.username}!\n"
                         f"Great you visited our bot for crypto traders. It's in beta for now.\n"
                         f"But some functions are available now, i.e. you can use the function "
                         f"of determining the correlation between the price of altcoin and bitcoin\n/help")


def register_start_command(dp: Dispatcher):
    dp.register_message_handler(command_start, CommandStart())
