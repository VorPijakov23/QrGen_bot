import asyncio  # Библиотека для асинхронного программирования
from os import getenv  # Метод для доступа к переменной окружения
from logging import basicConfig, INFO  # Методы для настройки логирования
from dotenv import load_dotenv   # Метод для инициализации файла .env

from aiogram import Dispatcher, Bot  # Импорт Dispatcher и Bot

from app.handlers import router  # Импорт роутера

load_dotenv()  # Инициализация .env

TOKEN = getenv("TOKEN")  # Константа с токеном бота

bot = Bot(token=TOKEN)  # Объект для запуска бота по токену
dp = Dispatcher()  # Основной объект для последующей обработки (впоследствии будет заменён на Router)


async def main() -> None:
    """Функция для запуска бота"""
    dp.include_router(router)  # Замена dp на router
    await dp.start_polling(bot)  # Ожидание ответов от серверов телеграма


if __name__ == '__main__':
    basicConfig(level=INFO)  # Настройка и запуск логирования
    try:
        asyncio.run(main())  # Запуск асинхронной функции main()
    except KeyboardInterrupt:
        print('Exit')  # Обработка исключения для досрочного выхода (CTRL+C)
