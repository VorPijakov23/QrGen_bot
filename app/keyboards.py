from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Inline main keyboard
main_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Генерация QR-Кода', callback_data='generate_qrcode')],
    [InlineKeyboardButton(text='Расшифровка QR-Кодов', callback_data='decode_qrcode')],
    [InlineKeyboardButton(text='Остальные проекты автора💼', callback_data='other_projects')],

])
# Inline info keyboard
info_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Десктопный QrGen', url='https://github.com/VorPijakov23/QrGen')],
    [InlineKeyboardButton(text='Пример бота aiogram', url='https://github.com/VorPijakov23/ExampleBot_aiogram3.4.1')],
    [InlineKeyboardButton(text='Cs_go_beta2.3', url='https://github.com/VorPijakov23/Cs_go3_beta2.3')],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')]
])

# Inline QR-Code generate
qr_gen_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сгенерировать по дефолту', callback_data='generate_default')],
    [InlineKeyboardButton(text='Изменить настройки QR-Кода', callback_data='edit_qr_setting')],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')]
])

# Inline back QR-Code
back_gen_default = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='gen_back')]
])

# Inline photo or url
qr_or_url = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расшифровка по фото', callback_data='with_photo')],
    [InlineKeyboardButton(text='Расшифровка по URL', callback_data='with_url')],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')]
])

# Inline back QR-decode
back_qr_decode = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='decode_back')]
])
