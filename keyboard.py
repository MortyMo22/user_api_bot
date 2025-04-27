# keyboard.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="📄 Показать текущую модель", callback_data="current_model"),
            InlineKeyboardButton(text="🔄 Сменить модель", callback_data="change_model"),
        ],
        [
            InlineKeyboardButton(text="🗑 Сбросить историю", callback_data="reset_history"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
