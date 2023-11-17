import logging
import os
import sys
from dotenv import load_dotenv
import asyncio
from aiogram import *
from aiogram.enums import ParseMode

from modules.handlers import *
from aiogram.filters import CommandStart, Command
from modules import questionaire, handlers
from modules.states import *

dotenv_path = 'data1/.env'
load_dotenv(dotenv_path)
BOT = os.getenv("TOKEN")


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(BOT, parse_mode=ParseMode.HTML)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(
        questionaire.router,
        handlers.router
    )

    dp.message.register(start, CommandStart())
    dp.callback_query.register(callback_func)

    # dp.message.register(settings, Command('настройки'))
    # dp.message.register(get_photo, F.audio)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_update=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


