# QR Code Telegram Bot
## Описание
### Этот Telegram-бот предназначен для генерации и расшифровки QR-кодов. Пользователи могут отправлять боту текстовые сообщения, которые он превращает в QR-коды, а также отправлять фотографии с QR-кодами для их расшифровки.

## Установка
### Клонируйте репозиторий на свой компьютер:

```bash
git clone https://github.com/VorPijakov23/QrGen_bot.git
```

### Установите зависимости:

```bash
pip install -r requirements.txt
```

### Создайте файл .env в корневой директории проекта и добавьте туда свои данные:
```bash
echo TOKEN=ваш_токен_от_телеграм > .env
```
### Запустите бота:

```bash
python main.py
```
### Использование
#### Бот умеет генерировать QR-коды с настройками по умолчанию, и с кастомными:
- Версия QR-кода (Фактический размер и количество "ячеек")
- Уровень коррекции ошибок. Соотношением доступной потери информации на разных уровнях:
1) L – 7%
2) M – 15%
3) Q – 25%
4) H – 30%
#### Есть возможность расшифровки QR-кодов как по url, так и путём отправки фото
#### Команды:
/start - начать общение с ботом.

/help - получить список команд и инструкцию по использованию.

/gengr - меню с настройками генерации QR-кода.

/decqr - меню с настройками расшифровкой QR-кода.
