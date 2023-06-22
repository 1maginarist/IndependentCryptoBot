import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.middlewares.inline_answer import IKMAnswerMiddleware
from tgbot.config import load_config

from tgbot.handlers import start
from tgbot.handlers import help
from tgbot.handlers import menu

logger = logging.getLogger(__name__)


# Registration order: Middleware -> Filters -> Handlers
def register_all_middlewares(dp):
    #dp.setup_middleware(IKMAnswerMiddleware)
    pass

def register_all_filters(dp):
    pass


def register_all_handlers(dp):
    start.register_start_command(dp)
    help.register_command_help(dp)
    menu.register_menu(dp)


async def main():

    # filename - name of the file
    # lineno - line number
    # levelname - level of logging (DEBUG, INFO, WARN, ERROR)
    # asctime - time
    # message - the core message'''

    logging.basicConfig(
        level=logging.DEBUG,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')

    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # to access config information from bot instance. Example - bot.get('config')
    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped')
