# bot.py
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from config import BOT_TOKEN, ADMIN_ID  # добавим свой ID сюда
from openai_api import chat_with_g4f, MODEL_PRIORITY
from keyboard import get_main_keyboard
from log import log_message

import asyncio
import os

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Память
user_model = {}
active_requests = {}  # user_id -> "Ожидает" или "Завершено"
last_messages = {}    # user_id -> последнее сообщение

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"
    text = message.text.strip()

    if text == "/start":
        await message.answer(
            "👋 Привет! Выбери действие:",
            reply_markup=get_main_keyboard()
        )
        return

    if text == "/status" and user_id == ADMIN_ID:
        status_report = "\n".join([
            f"👤 {uid}: {status} | Последнее: {last_messages.get(uid, '')[:30]}"
            for uid, status in active_requests.items()
        ]) or "Нет активных запросов."
        await message.answer(f"🛠 Статус запросов:\n\n{status_report}")
        return

    # Сохраняем что пользователь что-то спросил
    last_messages[user_id] = text
    active_requests[user_id] = "Ожидает ответа"

    # Сообщение про ожидание
    thinking_message = await message.answer("⌛ Обрабатываю твой запрос...")

    preferred_model = user_model.get(user_id)

    try:
        bot_response = await chat_with_g4f(text, preferred_model=preferred_model)
        await thinking_message.edit_text(bot_response, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_keyboard())

        log_message(user_id, username, text, bot_response)
        active_requests[user_id] = "Ответ отправлен ✅"

    except Exception as e:
        error_text = str(e)
        await thinking_message.edit_text(f"⚠️ Ошибка:\n{error_text}", reply_markup=get_main_keyboard())
        active_requests[user_id] = "Ошибка ❌"

@dp.callback_query(F.data == "current_model")
async def show_current_model(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    model = user_model.get(user_id, MODEL_PRIORITY[0])
    await callback_query.message.answer(f"📄 Текущая модель: `{model}`", parse_mode=ParseMode.MARKDOWN)

@dp.callback_query(F.data == "change_model")
async def change_model(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    current = user_model.get(user_id, MODEL_PRIORITY[0])
    try:
        idx = MODEL_PRIORITY.index(current)
        new_model = MODEL_PRIORITY[(idx + 1) % len(MODEL_PRIORITY)]
    except:
        new_model = MODEL_PRIORITY[0]

    user_model[user_id] = new_model
    await callback_query.message.answer(f"✅ Модель сменена на `{new_model}`", parse_mode=ParseMode.MARKDOWN)

@dp.callback_query(F.data == "reset_history")
async def reset_history(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        os.remove(f"logs/{user_id}.log")
        await callback_query.message.answer("🗑 История сообщений сброшена!")
    except:
        await callback_query.message.answer("⚠️ Нет истории для удаления.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
