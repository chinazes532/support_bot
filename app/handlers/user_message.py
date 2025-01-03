from typing import cast

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.filters.admin_filter import AdminProtect

from app.database import insert_user, get_user, update_topic_id

from app.states import Ask

from config import CHAT_ID, ADMINS

user = Router()


@user.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)

    if not user:
        await message.answer(f"Привет, {message.from_user.full_name}!\n",
                             reply_markup=ikb.user_panel)

        await insert_user(user_id, message.from_user.full_name, None)
    else:
        await message.answer(f"Привет, {message.from_user.full_name}! (ok)\n",
                             reply_markup=ikb.user_panel)

    for admin in ADMINS:
        if user_id == admin:
            await message.answer("Вы успешно авторизовались как администратор!",
                                 reply_markup=rkb.admin_menu)
            return


@user.callback_query(F.data == "ask_question")
async def ask_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"Отправьте свой вопрос!",
                                  reply_markup=ikb.user_cancel)

    await state.set_state(Ask.question)


@user.message(Ask.question)
async def get_question(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    user = await get_user(user_id)
    if user[2] is None:
        try:
            # Создаем новый форумный топик
            forum_topic = await bot.create_forum_topic(chat_id=CHAT_ID, name=f"{message.from_user.full_name} "
                                                                             f"(@{message.from_user.username})")
            print(forum_topic)
            print(forum_topic.message_thread_id)

            # Получаем ID созданного топика
            topic_id = forum_topic.message_thread_id

            await bot.copy_message(chat_id=CHAT_ID,
                                   from_chat_id=message.chat.id,
                                   message_id=message.message_id,
                                   reply_to_message_id=topic_id)

            # Отправляем уведомление пользователю
            await message.answer("Вопрос успешно отправлен!",
                                 reply_markup=ikb.user_panel)

            # Логируем вопро
            await update_topic_id(user_id, topic_id)

            # Очищаем состояние
            await state.clear()
        except Exception as e:
            await message.answer("Произошла ошибка при отправке вопроса. Пожалуйста, попробуйте позже.")
            print(f"Ошибка: {e}")
    else:
        try:
            await bot.copy_message(chat_id=CHAT_ID,
                                   from_chat_id=message.chat.id,
                                   message_id=message.message_id,
                                   reply_to_message_id=user[2])

            # Отправляем уведомление пользователю
            await message.answer("Вопрос успешно отправлен!",
                                 reply_markup=ikb.user_panel)

            await state.clear()
        except Exception as e:
            await message.answer("Произошла ошибка при отправке вопроса. Пожалуйста, попробуйте позже.")
            print(f"Ошибка: {e}")


@user.callback_query(F.data == "user_cancel")
async def user_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(f"Привет, {callback.from_user.full_name}!\n",
                             reply_markup=ikb.user_panel)