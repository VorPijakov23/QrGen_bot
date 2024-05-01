import json
from re import compile
from os import getenv

from requests import get
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode
from dotenv import load_dotenv

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

import app.keyboards as kb

load_dotenv()

router = Router()
# f'qrcodes_files/download_temp_{message.from_user.id}.png'
URI = f"https://api.telegram.org/file/bot{getenv('TOKEN')}/"


async def dec(image_path) -> str:
    """Инкапсулированный метод для расшифровки сохранённого QR-кода"""
    try:
        img = Image.open(image_path)
        res = '\n\n'.join([i.data.decode('utf-8') for i in decode(img)])
        return f"Расшифрованные QR-Коды:\n {res}"
    except FileNotFoundError:
        return "Файл не найден"
'''    except Exception:
        return f"Произошла ошибка"'''


async def download_image(url, file_name):
    # Отправляем GET-запрос на URL-адрес изображения
    response = get(url)
    name: str = file_name

    # Проверяем, что запрос был успешным
    if response.status_code == 200:
        # Пытаемся открыть изображение с помощью Pillow
        try:
            image = Image.open(BytesIO(response.content))
            # Сохраняем изображение
            image.save(name)
            return True
        except IOError:
            return False


async def decode_qrcode(url, temp_file_name) -> str:
    if not await download_image(url=url, file_name=temp_file_name):
        return 'Произошла ошибка в чтении QR-Кода'
    res = await dec(image_path=temp_file_name)
    return res


class Gen(StatesGroup):
    state_qenerate_default = State()
    state_edit_qr_version = State()
    state_edit_qr_err = State()
    state_qenerate_text = State()
    state_decode_url = State()


# Раздел Commands
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text='Привет, я - ваш помощник в генерации и расшифровки QR-кодов.\n'
                              'Нажми /help для ознакомления')
    await message.answer(text='Меню©️', reply_markup=kb.main_inline_kb)


@router.message(Command('help', ignore_case=True))
async def cmd_help(message: Message):
    await message.answer(text='Основные функции бота:\n1) Генерация QR-Кода\n2) Расшифровка QR-Кода\n\n'
                              'Бот был создан в целях демонстрации работы проекта'
                              ' (Подробнее можно ознакомится в разделе /other)\n\n'
                              '/gengr - Генерация QR-кода\n'
                              '/decqr - Расшифровка QR-кода\n'
                              '/menu - Для открытия меню с действиями')


@router.message(Command('gengr', ignore_case=True))
async def cmd_genqr(message: Message):
    await message.answer(text='Выберите пункт ниже: ', reply_markup=kb.qr_gen_inline_keyboard)


@router.message(Command('decqr', ignore_case=True))
async def cmd_decqr(message: Message):
    await message.answer(text='Выберите пункт:', reply_markup=kb.qr_or_url)


@router.message(Command('other', ignore_case=True))
async def cmd_other(message: Message):
    await message.answer(text=f"Остальные проекты [VorPijakov23](https://github.com/VorPijakov23):",
                         parse_mode='Markdown', disable_web_page_preview=True, reply_markup=kb.info_inline_kb)


@router.message(Command('menu', ignore_case=True))
async def cmd_menu(message: Message):
    await message.answer(text='Меню©️', reply_markup=kb.main_inline_kb)


# Раздел CallBacks
@router.callback_query(F.data == 'generate_qrcode')
async def call_genqr(callback: CallbackQuery):
    await callback.message.edit_text(text='Выберите пункт ниже: ', reply_markup=kb.qr_gen_inline_keyboard)


@router.callback_query(F.data == 'decode_qrcode')
async def call_decqr(callback: CallbackQuery):
    await callback.message.edit_text(text='Выберите пункт:', reply_markup=kb.qr_or_url)


@router.callback_query(F.data == 'with_url')
async def call_with_url(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.state_decode_url)
    await callback.message.edit_text('Введите URL QR-Кода:', reply_markup=kb.back_qr_decode)


@router.callback_query(F.data == "other_projects")
async def call_other(callback: CallbackQuery):
    await callback.answer()
    link_text = "VorPijakov23"
    url = "https://github.com/VorPijakov23"
    markdown_link = f"Остальные проекты [{link_text}]({url}):"
    await callback.message.edit_text(markdown_link, parse_mode="Markdown",
                                     disable_web_page_preview=True, reply_markup=kb.info_inline_kb)


@router.callback_query(F.data == "main_menu")
async def call_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(text='Меню©️', reply_markup=kb.main_inline_kb)


@router.callback_query(F.data == 'edit_qr_setting')
async def call_edit_qr_setting(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.state_edit_qr_version)
    await callback.message.edit_text('Введите версию QR-кода (1 - 9; 10 - 26; 27 - 40): ',
                                     reply_markup=kb.back_gen_default)


@router.callback_query(F.data == 'generate_default')
async def call_qenerate_default(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.state_qenerate_default)
    await callback.message.edit_text(text='Введите текст для кодирования в QR-код: ', reply_markup=kb.back_gen_default)


@router.callback_query(F.data == 'gen_back')
async def call_gen_back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Выберите пункт ниже: ', reply_markup=kb.qr_gen_inline_keyboard)
    await state.clear()


@router.callback_query(F.data == 'decode_back')
async def call_back_decode(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Выберите пункт:', reply_markup=kb.qr_or_url)
    await state.clear()


# Состояния
@router.message(Gen.state_qenerate_default)
async def state__qenerate_default(message: Message, state: FSMContext):
    if len(message.text) >= 200:
        await message.answer(text='Текст должен быть меньше 200 символов')
        await state.clear()
        await message.answer(text='Меню©️', reply_markup=kb.main_inline_kb)
    else:
        with open("conf.json", "r", encoding='utf-8') as f:
            config = json.load(f)
        version: int = int(config['qr_version'])  # Версия QR кода
        box_size: int = int(config['box_size'])  # Размер QR-кода
        border: int = int(config['border'])  # Количество пустого пространства
        fill_color: str = config['fill_color']  # Цвет для самого QR кода
        back_color: str = config['back_color']  # Цвет фона
        # уровни восстановления ошибок
        error_correction: str = config['error_correction'].upper()
        dep: dict = {
            'L': ERROR_CORRECT_L,
            'M': ERROR_CORRECT_M,
            'Q': ERROR_CORRECT_Q,
            'H': ERROR_CORRECT_H
        }
        file_name = f'qrcodes_files/temp_{message.from_user.id}.png'
        get_file_name = FSInputFile(file_name)
        try:
            qr = QRCode(
                version=version,
                error_correction=dep[error_correction],
                box_size=box_size,
                border=border
            )

            qr.add_data(message.text)
            qr.make()

            img = qr.make_image(fill_color=fill_color,
                                back_color=back_color)
            img.save(file_name)
            await message.answer_photo(photo=get_file_name, caption=f"1) Кодированный текст > {message.text}\n"
                                                                    f"2) Версия QR-кода > {version}\n"
                                                                    f"3) Размер QR-кода > {box_size}\n"
                                                                    f"4) Количество пустого пространства > {border}\n"
                                                                    f"5) Цвет QR-кода > {fill_color}\n"
                                                                    f"6) Цвет фона > {back_color}\n"
                                                                    f"7) Уровень восстановления ошибок (L, M, Q, H) >"
                                                                    f" {error_correction}")
        except ImportError:
            print("Ошибка в импорте библиотек")
        except KeyboardInterrupt:
            print('\nExit')
        except EOFError:
            print("EOFError")
        finally:
            await state.clear()
            await message.answer(text='Меню©️', reply_markup=kb.main_inline_kb)


@router.message(Gen.state_decode_url)
async def state__decode_url(message: Message, state: FSMContext):
    if compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+').match(message.text):
        res = await decode_qrcode(url=message.text,
                                  temp_file_name=f'qrcodes_files/download_temp_{message.from_user.id}.png')
        await message.answer(res)
    else:
        await message.answer('Это не URL')
        await message.answer(text='Меню©️', reply_markup=kb.main_inline_kb)
        await state.clear()


@router.message(Gen.state_edit_qr_version)
async def state__edit_qr_version(message: Message, state: FSMContext):
    user_answer = message.text
    if user_answer in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                       '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
                       '34', '35', '36', '37', '38', '39', '40']:
        await state.update_data(ver=message.text)
        await state.set_state(Gen.state_edit_qr_err)
        await message.answer('Введите уровень восстановления ошибок (L, M, Q, H)', reply_markup=kb.back_gen_default)
    else:
        await message.answer('Не верный ввод')
        await state.clear()
        await message.answer(text='Меню©️', reply_markup=kb.main_inline_kb)


@router.message(Gen.state_edit_qr_err)
async def state__edit_qr_err(message: Message, state: FSMContext):
    if message.text.upper() in ['L', "M", "Q", "H"]:
        await state.update_data(err_cor=message.text)
        await state.set_state(Gen.state_qenerate_text)
        await message.answer(text='Введите текст для кодирования в QR-код:', reply_markup=kb.back_gen_default)
    else:
        await message.answer('Не верный ввод')
        await state.clear()
        await message.answer(text='Меню©️', reply_markup=kb.main_inline_kb)


@router.message(Gen.state_qenerate_text)
async def state__qenerate_text(message: Message, state: FSMContext):
    if len(message.text) <= 200:
        data = await state.get_data()
        version = data['ver']
        err_cor: str = data['err_cor'].upper()
        with open("conf.json", "r", encoding='utf-8') as f:
            config = json.load(f)

        box_size: int = int(config['box_size'])  # Размер QR-кода
        border: int = int(config['border'])  # Количество пустого пространства
        fill_color: str = config['fill_color']  # Цвет для самого QR кода
        back_color: str = config['back_color']  # Цвет фона
        dep: dict = {
            'L': ERROR_CORRECT_L,
            'M': ERROR_CORRECT_M,
            'Q': ERROR_CORRECT_Q,
            'H': ERROR_CORRECT_H
        }

        file_name = f'qrcodes_files/temp_{message.from_user.id}.png'
        get_file_name = FSInputFile(file_name)
        try:
            qr = QRCode(
                version=version,
                error_correction=dep[err_cor],
                box_size=box_size,
                border=border
            )

            qr.add_data(message.text)
            qr.make()

            img = qr.make_image(fill_color=fill_color,
                                back_color=back_color)
            img.save(file_name)
            await message.answer_photo(photo=get_file_name, caption=f"1) Кодированный текст > {message.text}\n"
                                                                    f"2) Версия QR-кода > {version}\n"
                                                                    f"3) Размер QR-кода > {box_size}\n"
                                                                    f"4) Количество пустого пространства > {border}\n"
                                                                    f"5) Цвет QR-кода > {fill_color}\n"
                                                                    f"6) Цвет фона > {back_color}\n"
                                                                    f"7) Уровень восстановления ошибок (L, M, Q, H) >"
                                                                    f" {err_cor}")
        except ImportError:
            print("Ошибка в импорте библиотек")
        except KeyboardInterrupt:
            print('\nExit')
        except EOFError:
            print("EOFError")
        finally:
            await state.clear()
            await message.answer(text='Меню©️', reply_markup=kb.main_inline_kb)

    else:
        await message.answer(text='Текст должен быть меньше 200 символов')
        await state.clear()
        await message.answer(text='Меню©️', reply_markup=kb.main_inline_kb)


# Обработчик фото
@router.message(F.photo)
async def _photo(message: Message):
    file_name = f'qrcodes_files/download_from_user_temp_{message.from_user.id}.png'
    file_id = message.photo[-1].file_id
    await message.bot.download(file=file_id, destination=file_name)
    res = await dec(file_name)
    await message.answer(text=res)


# Исключение
@router.message()
async def _other(message: Message):
    await message.answer(text='Нет такой функции')
