# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
import requests

from keyboards.reply_z_all import menu_frep
from loader import dp, bot

# Колбэк с удалением сообщения
from services.dbhandler import get_all_users_id


@dp.callback_query_handler(text="close_this", state="*")
async def processing_callback_remove(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

@dp.callback_query_handler(text_startswith="close_message", state="*")
async def processing_callback_remove(call: CallbackQuery, state: FSMContext):
    id = int(call.data.split(":")[1])
    print(id)
    await bot.delete_message(call.from_user.id, message_id=id)

# Колбэк с обработкой кнопки
@dp.callback_query_handler(text="...", state="*")
async def processing_callback_answer(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)


# Обработка всех колбэков которые потеряли стейты после перезапуска скрипта
@dp.callback_query_handler(state="*")
async def processing_callback_missed(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except:
        pass

    await call.message.answer("<b>❌ Данные не были найдены из-за перезапуска скрипта.\n"
                              "♻ Выполните действие заново.</b>",
                              reply_markup=menu_frep(call.from_user.id))


# Обработка всех неизвестных команд
@dp.message_handler()
async def processing_message_missed(message: Message):
    if message.text.startswith("/start ") and int(message.text.split()[1]) in get_all_users_id():
        await message.answer(f"<b>👋 Приветик {message.from_user.first_name}!</b>\n"
                         "❤️ Добро пожаловать в самый лучший магазин, по продаже Discord Nitro!!!\n"
                         " ——————————————————————————\n"\
                         "🛠 Технический Администратор : @Nikonoon",
                         reply_markup=menu_frep(message.from_user.id))
    else:
        if message.chat.id > 0:
            await message.answer("♦ Неизвестная команда.\n"
                             "▶ Введите /start")
