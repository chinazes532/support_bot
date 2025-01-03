from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Текст 1", callback_data="text_1")],
    ]
)

user_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Задать вопрос", callback_data="ask_question")],
    ]
)

user_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="user_cancel")],
    ]
)