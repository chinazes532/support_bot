from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.filters.admin_filter import AdminProtect
from app.filters.chat_type import ChatTypeFilter

from app.database import get_questions_and_delete
from config import CHAT_ID

admin = Router()


@admin.message(AdminProtect(), Command("admin"))
@admin.message(AdminProtect(), F.text == "Админ-панель")
async def admin_panel(message: Message):
    await message.answer(f"Вы вошли в админ-панель!\n"
                         f"Выберите действие",
                         reply_markup=ikb.admin_panel)


@admin.message(F.reply_to_message)
async def get_question(message: Message, bot: Bot):
    print(message.reply_to_message.message_thread_id)

    user_id = await get_questions_and_delete(message.reply_to_message.message_thread_id)

    if user_id is None:
        print("User ID not found.")
        return  # Можно также отправить сообщение об ошибке, если это необходимо

    print(user_id)

    await bot.copy_message(chat_id=user_id,
                           from_chat_id=message.chat.id,
                           message_id=message.message_id)




