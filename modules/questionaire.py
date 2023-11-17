from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from modules.states import *
from data1.db_main import *
from modules.keyboards import *

router = Router()


@router.message(Command('Добавить_категорию'))
async def add_categorie(message: Message, state: FSMContext):
    await state.set_state(Categories.name)
    await message.answer("Напишите название новой категории...", reply_markup=cancellation)


@router.message(Categories.name)
async def form_record(message: Message, state: FSMContext):
    cat = await db_add_categorie(message.from_user.id, message.text)
    if cat:
        await message.answer(cat)
    else:
        await state.clear()
        await message.answer('Добавлено', reply_markup=settings)


@router.message(Command('потратил'))
async def fill_profile(message: Message, state: FSMContext):
    await state.set_state(Form.record)
    await message.answer("Введи сумму...", reply_markup=cancellation)


@router.message(Command('Отмена'))
async def cancellation_commands(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отмена записи', reply_markup=main_kb)


@router.message(Form.record)
async def form_record(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(telegarm_id=message.from_user.id, record=message.text)
        await (state.set_state(Form.categories))
        await message.answer('Выберете категорию', reply_markup=await kb_categories(message.from_user.id))
    else:
        await message.reply('Это не сумма!!! Введите число!!!')


@router.message(Form.categories)
async def form_age(message: Message, state: FSMContext):
    if message.text in await db_select_categories(message.from_user.id):
        await state.update_data(categories=message.text)
        await state.set_state(Form.text)
        await message.answer(
            "Можете добавить текс к записи",
            reply_markup=kb_records_text)
    else:
        await message.reply('Выберете категорию из меню!!!')


@router.message(Form.text)
async def form_age(message: Message, state: FSMContext):
    if message.text == 'Не надо':
        await state.update_data(text=None)
    else:
        await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()
    await db_add_record(data)
    user = message.from_user.id
    await message.answer(f'Запись добавлена\n\n'
                         f"<i>Траты сегодня: {await db_select_spending(user, days='today')}"
                         f"{await db_select_currency(user)}</i>",
                         reply_markup=main_kb)

