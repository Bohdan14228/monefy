from aiogram.types import *
from data1.db_main import *
from enum import Enum

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/потратил'),
            KeyboardButton(text='/получил'),
        ],
        [KeyboardButton(text='настройки')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Enter text',
    selective=True
)


async def kb_categories(user):
    list1 = []
    l = []
    cat = await db_select_categories(user)  # Дождитесь завершения асинхронной функции
    for i in cat:
        l.append(KeyboardButton(text=i))
        if len(l) == 3:
            list1.append(l)
            l = []
    if l:
        list1.append(l)
    list1.append([KeyboardButton(text='/Отмена')])
    return ReplyKeyboardMarkup(keyboard=list1,
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder='Enter text',
                               selective=True
                               )


cancellation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/Отмена')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Enter text',
    selective=True
)

kb_records_text = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Не надо')
        ],
        [KeyboardButton(text='/Отмена')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Enter text',
    selective=True
)

settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Траты за период'),
            KeyboardButton(text='Записи')
        ],
        [
            KeyboardButton(text='Выбор валюты'),
            KeyboardButton(text='/Добавить_категорию')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Enter text',
    selective=True
)

kb_currency = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='UAH', callback_data='currency_UAH')],
        [InlineKeyboardButton(text='USD', callback_data='currency_USD')],
        [InlineKeyboardButton(text='EUR', callback_data='currency_EUR')]
    ]
)

kb_expenses_for_the_period = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='За сегодня', callback_data='За сегодня')],
        [InlineKeyboardButton(text='Неделю', callback_data='Неделю')],
        [InlineKeyboardButton(text='Месяц', callback_data='Месяц')],
        [InlineKeyboardButton(text='Все месяцы', callback_data='Все месяцы')],
        [InlineKeyboardButton(text='Всё', callback_data='Всё')],
        [InlineKeyboardButton(text='Отмена', callback_data='Отмена')],
    ]
)


async def kb_select_spending_by_group(currency, user, days):
    list1 = []
    cat = await db_select_spending_by_group(user, days)
    if cat:
        if days == 'last_7_days':
            for i in cat:
                list1.append([InlineKeyboardButton(text=f"{i[0]}: {i[1]} {currency}",
                                                   callback_data=f'{i[0]} last_7_days')])
        else:
            for i in cat:
                list1.append([InlineKeyboardButton(text=f"{i[0]}: {i[1]} {currency}", callback_data=f'{i[0]}')])
        list1.append([InlineKeyboardButton(text='Назад', callback_data='Назад')])
        list1 = InlineKeyboardMarkup(inline_keyboard=list1)
    else:
        list1 = main_kb
    return list1


# async def kb_select_spending_specific_date(currency, user, date):
#     list1 = []
#     cat = await db_select_spending_specific_date(user, date)
#     if cat:
#         for i in cat:
#             list1.append([InlineKeyboardButton(text=f"{i[0]}: {i[1]} {currency}", callback_data=f'{i[0]}')])
#         list1.append([InlineKeyboardButton(text='Назад', callback_data='Назад')])
#         list1 = InlineKeyboardMarkup(inline_keyboard=list1)
#     else:
#         list1 = main_kb
#     return list1


async def kb_select_spending_last_7_days(currency, user):
    list1 = []
    cat = await db_select_spending(user, 'last_7_days')
    if cat:
        for i in cat:
            list1.append([InlineKeyboardButton(text=f"{i[0]}: {i[1]} {currency}", callback_data=f'{i[0]}')])
        list1.append([InlineKeyboardButton(text='Назад', callback_data='Назад')])
        list1 = InlineKeyboardMarkup(inline_keyboard=list1)
    else:
        list1 = main_kb
    return list1


async def kb_select_spending_summary_by_month(currency, user):
    list1 = []
    cat = await db_select_spending(user, 'summary_by_month')
    if cat:
        for month, sum1 in cat:
            list1.append([InlineKeyboardButton(text=f"{month}: {sum1} {currency}", callback_data=f'{month}')])
        list1.append([InlineKeyboardButton(text='Назад', callback_data='Назад')])
        list1 = InlineKeyboardMarkup(inline_keyboard=list1)
    else:
        list1 = main_kb
    return list1


async def kb_change_records(id_rec):
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Изменить', callback_data=f'Изменить_{id_rec}')]])
    return ikb


# kb_categories_settings = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text='Добавить категорию', callback_data=f'Добавить категорию')]
#         ])
