from aiogram import types
from aiogram import Bot, Router
import os
from dotenv import load_dotenv
from data1.db_main import *
from modules import keyboards
from data1.db_main import *
from aiogram.types import *
from data1.shara import pattern


dotenv_path = 'data1/.env'
load_dotenv(dotenv_path)
ID = os.getenv("ID")

router = Router()


async def start_bot(bot: Bot):
    await bot.send_message(ID, 'Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(ID, 'Бот остановлен!')


async def start(message: types.Message):
    # await message.answer('<s>зачеркнутое</s>')
    # await message.answer('<tg-spoiler>зачеркнутое</tg-spoiler>')
    if message.from_user.last_name is None:
        name = f"{message.from_user.first_name}"
    else:
        name = f"{message.from_user.first_name} {message.from_user.last_name}"
    mes = f'Привіт, {name}'
    await message.answer(mes, reply_markup=keyboards.main_kb)
    await db_add_user(message.from_user.id)
    await db_add_categories(message.from_user.id)


@router.message()
async def settings(message: types.Message):
    if message.text == 'настройки':
        await message.answer('настройки', reply_markup=keyboards.settings)

    elif message.text == 'Выбор валюты':
        await message.answer('Выберете валюту', reply_markup=keyboards.kb_currency)

    elif message.text == 'Назад':
        await message.answer('Назад', reply_markup=keyboards.main_kb)

    elif message.text == 'Траты за период':
        await message.answer('Выбери', reply_markup=keyboards.kb_expenses_for_the_period)

    # elif message.text == 'Категории':
    #     await message.answer('Выбери', reply_markup=)


async def callback_func(callback: types.CallbackQuery):
    if callback.data.startswith('currency'):
        currency = callback.data.split('_')[-1]
        await db_currency_setting(currency, callback.from_user.id)
        await callback.message.answer(f'Валюта изменена на <i>{currency}</i>', reply_markup=keyboards.settings)

    elif callback.data == 'За сегодня':
        user = callback.from_user.id
        currency = await db_select_currency(user)
        await callback.message.answer(f'<b>Траты сегодня: '
                                      f"{await db_select_spending(user, 'today')} {currency}</b>\n",
                                      reply_markup=await keyboards.kb_select_spending_by_group(currency, user, 'today'))

    elif callback.data == 'Неделю':
        user = callback.from_user.id
        currency = await db_select_currency(user)
        await callback.message.answer(f'<b>Траты за неделю: '
                                      f"{sum([i[-1] for i in await db_select_spending(user, 'last_7_days')])} "
                                      f"{currency}</b>\n",
                                      reply_markup=await keyboards.kb_select_spending_by_group(currency, user,
                                                                                               'last_7_days'))

    elif callback.data.split()[0] in categories and callback.data.endswith('last_7_days'):
        currency = await db_select_currency(callback.from_user.id)
        cat = await db_select_spending_specific_categorie_last_7_days(callback.from_user.id, callback.data.split()[0])

        for id_rec, record, text, date in cat:
            str1 = ""
            date = '.'.join(date.split()[0].split('-')[::-1])
            if text:
                str1 += f"<b>{record} {currency}</b>\n<i>{text}</i>\n{date}"
            else:
                str1 += f"<b>{record} {currency}</b>\n{date}"
            await callback.message.answer(str1,
                                          reply_markup=await keyboards.kb_change_records(id_rec))

    elif callback.data == 'Месяц':
        user = callback.from_user.id
        currency = await db_select_currency(user)
        await callback.message.answer(f'<b>Траты за месяц: '
                                      f"{sum([i[-1] for i in await db_select_spending(user, 'summary_by_month')])} "
                                      f"{currency}</b>\n",
                                      reply_markup=await keyboards.kb_select_spending_summary_by_month(currency, user))

    elif callback.data == 'Назад':
        await callback.message.delete()

    else:
        await callback.message.delete()
        await callback.message.answer('Меню', reply_markup=keyboards.main_kb)

# async def get_photo(message: types.Message, bot: Bot):
#     await message.answer('Ты отправил картинку, я сохранил её себе')
#     file = await bot.get_file(message.photo[-1].file_id)
#     await bot.download_file(file.file_path, 'photo.jpg')
#

# async def input_record(message: types.Message):
#     if message.text.isdigit():

