import asyncio
import os

from services.ai_generation import generate_image_mock
from database.db import init_db, save_generation
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from keyboards.main_menu import main_menu, after_result_menu, start_keyboard
from aiogram import F
from aiogram.fsm.context import FSMContext
from states.user_states import UserStates
from aiogram.types import Message, CallbackQuery, FSInputFile
from config import BOT_TOKEN
from prompts.generation_prompts import (
    HAIRCUT_BOARD_PROMPT,
    COLOR_BOARD_PROMPT,
    STYLE_IDENTITY_PROMPT,
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def show_main_menu(message: Message):
    await message.answer(
        "Кнопка «Главное меню» теперь доступна внизу.",
        reply_markup=start_keyboard
    )

    await message.answer(
        "Привет!\n\n"
        "Выберите функцию:",
        reply_markup=main_menu
    )

async def save_user_photo(message: Message, bot: Bot, task_name: str) -> str:
    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)

    os.makedirs("downloads", exist_ok=True)

    file_path = f"downloads/{message.from_user.id}_{task_name}.jpg"

    await bot.download_file(file.file_path, file_path)

    return file_path

@dp.message(CommandStart())
async def start_handler(message: Message):
    await show_main_menu(message)

@dp.message(F.text == "Главное меню")
async def main_menu_button_handler(message: Message):
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu
    )

@dp.callback_query()
async def process_menu(callback: CallbackQuery, state: FSMContext):

    if callback.data == "main_menu":
        await callback.message.answer(
            "Главное меню:",
            reply_markup=main_menu
        )

    elif callback.data == "haircut_board":
        await state.update_data(last_task="haircut_board")
        await state.set_state(UserStates.waiting_photo_for_haircut_board)
        await callback.message.answer(
            "Загрузите фотографию для генерации борда по стрижкам."
        )

    elif callback.data == "color_board":
        await state.update_data(last_task="color_board")
        await state.set_state(UserStates.waiting_photo_for_color_board)
        await callback.message.answer(
            "Загрузите фотографию для генерации борда по окрашиваниям."
        )

    elif callback.data == "style_identity":
        await state.update_data(last_task="style_identity")
        await state.set_state(UserStates.waiting_photo_for_style_identity_board)
        await callback.message.answer(
            "Загрузите фотографию для создания Style Identity Board."
        )

    elif callback.data == "generate_again":
        data = await state.get_data()
        last_task = data.get("last_task")

        if last_task == "haircut_board":
            await state.set_state(UserStates.waiting_photo_for_haircut_board)
            await callback.message.answer(
                "Загрузите новое фото для генерации борда по стрижкам."
            )

        elif last_task == "color_board":
            await state.set_state(UserStates.waiting_photo_for_color_board)
            await callback.message.answer(
                "Загрузите новое фото для генерации борда по окрашиваниям."
            )

        elif last_task == "style_identity":
            await state.set_state(UserStates.waiting_photo_for_style_identity_board)
            await callback.message.answer(
                "Загрузите новое фото для создания Style Identity Board."
            )

        else:
            await callback.message.answer(
                "Сначала выберите функцию:",
                reply_markup=main_menu
            )

    await callback.answer()

@dp.message(UserStates.waiting_photo_for_haircut_board, F.photo)
async def get_haircut_photo(message: Message, state: FSMContext):
    file_path = await save_user_photo(message, bot, "haircut")

    await state.set_state(UserStates.generating)

    await message.answer("Фото получено. Генерирую борд по стрижкам...")

    try:
        result_path = await generate_image_mock(
            file_path,
            HAIRCUT_BOARD_PROMPT
        )

        save_generation(
            user_id=message.from_user.id,
            username=message.from_user.username,
            task_type="haircut_board",
            photo_path=file_path,
            result_path=result_path
        )

        await state.set_state(UserStates.result_ready)

        await message.answer_photo(
            photo=FSInputFile(result_path),
            caption="Готово! Борд по стрижкам.",
            reply_markup=after_result_menu
        )

    except Exception as error:
        print(error)

        await state.set_state(UserStates.error)

        await message.answer(
            f"❌ Ошибка генерации:\n\n{error}",
            reply_markup=after_result_menu
        )

    await state.clear()

@dp.message(UserStates.waiting_photo_for_color_board, F.photo)
async def get_color_photo(message: Message, state: FSMContext):
    file_path = await save_user_photo(message, bot, "color")

    await state.set_state(UserStates.generating)

    await message.answer("Фото получено. Генерирую борд по окрашиваниям...")

    try:
        result_path = await generate_image_mock(
            file_path,
            COLOR_BOARD_PROMPT
        )

        save_generation(
            user_id=message.from_user.id,
            username=message.from_user.username,
            task_type="color_board",
            photo_path=file_path,
            result_path=result_path
        )

        await state.set_state(UserStates.result_ready)

        await message.answer_photo(
            photo=FSInputFile(result_path),
            caption="Готово! Борд по окрашиваниям.",
            reply_markup=after_result_menu
        )

    except Exception as error:
        print(error)

        await state.set_state(UserStates.error)

        await message.answer(
            "❌ Ошибка генерации изображения.\n\n"
            "Проверьте интернет-соединение или попробуйте позже.",
            reply_markup=after_result_menu
        )

    await state.clear()


@dp.message(UserStates.waiting_photo_for_style_identity_board, F.photo)
async def get_style_identity_photo(message: Message, state: FSMContext):
    file_path = await save_user_photo(message, bot, "style_identity")

    await state.set_state(UserStates.generating)

    await message.answer("Фото получено. Создаю Style Identity Board...")

    try:
        result_path = await generate_image_mock(
            file_path,
            STYLE_IDENTITY_PROMPT
        )

        save_generation(
            user_id=message.from_user.id,
            username=message.from_user.username,
            task_type="style_identity_board",
            photo_path=file_path,
            result_path=result_path
        )

        await state.set_state(UserStates.result_ready)

        await message.answer_photo(
            photo=FSInputFile(result_path),
            caption="Готово! Style Identity Board.",
            reply_markup=after_result_menu
        )

    except Exception as error:
        print(error)

        await state.set_state(UserStates.error)

        await message.answer(
            "❌ Ошибка генерации изображения.\n\n"
            "Проверьте интернет-соединение или попробуйте позже.",
            reply_markup=after_result_menu
        )

    await state.clear()

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
