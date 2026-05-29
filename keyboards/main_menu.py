from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Стрижки",
                callback_data="haircut_board"
            )
        ],
        [
            InlineKeyboardButton(
                text="Окрашивания",
                callback_data="color_board"
            )
        ],
        [
            InlineKeyboardButton(
                text="Сделать стилевую карту / Style Identity Board",
                callback_data="Сделать стилевую карту / Style Identity Board"
            )
        ]
    ]
)

after_result_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Сгенерировать ещё",
                callback_data="generate_again"
            )
        ],
        [
            InlineKeyboardButton(
                text="Выбрать другую функцию",
                callback_data="main_menu"
            )
        ]
    ]
)

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главное меню")
        ]
    ],
    resize_keyboard=True
)