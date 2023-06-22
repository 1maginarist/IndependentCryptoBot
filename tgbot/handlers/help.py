from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandHelp


async def command_help(message: types.Message):
    await message.answer("List of available commands:\n"
                         " - /start - get welcome message\n"
                         "- /help - to get help message\n"
                         "- /menu - enter main menu\n"
                         "- /back - return to previous menu page")


def register_command_help(dp: Dispatcher):
    dp.register_message_handler(command_help, CommandHelp())