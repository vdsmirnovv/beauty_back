import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from app.db import SessionLocal
from app import crud, schemas


# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


TELEGRAM_TOKEN = '7237687305:AAHv5aZn2OYWIf9AMY_SAK1Gltv9cVwOI-w'

# Функция /start, которая вызывается при старте
async def start(update: Update, context: CallbackContext):
    # Кнопка для отправки контакта
    button = KeyboardButton("Поделиться контактом", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True)
    await update.message.reply_text(
        "Привет! Я бот студии красоты. Пожалуйста, поделитесь своим контактом для регистрации.",
        reply_markup=reply_markup
    )

# Функция для регистрации нового пользователя
async def register(update: Update, context: CallbackContext):
    user_telegram_id = update.message.from_user.id
    contact = update.message.contact

    if contact:
        full_name = update.message.from_user.full_name
        phone_number = contact.phone_number

        # Создаём нового пользователя в базе
        db = SessionLocal()
        new_user = crud.create_user(db, schemas.UserCreate(
            telegram_id=str(user_telegram_id),
            full_name=full_name,
            phone_number=phone_number
        ))


        await update.message.reply_text(
            f"Ты зарегистрирован как {new_user.full_name}!\n"
            f"Номер телефона: {new_user.phone_number}. Регистрация прошла успешно!"
        )

   
        
        web_app_url = "https://beauty-app-seven.vercel.app"  
        web_app_button = InlineKeyboardButton(
            text="Открыть веб-приложение",
            web_app=WebAppInfo(url=web_app_url)
        )

        reply_markup = InlineKeyboardMarkup([[web_app_button]])

        await update.message.reply_text(
            "Нажми на кнопку, чтобы открыть веб-приложение 👇",
            reply_markup=reply_markup
        )

        db.close()
    else:
        await update.message.reply_text("Пожалуйста, отправьте свой контактный номер.")

# Обработчик для текста
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    # Если сообщение не команда, отправляем запрос на контакт
    if not update.message.text.startswith('/'):
        await start(update, context)

# Основная функция, которая запускает бота
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Обработчик для текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Обработчик для контактов
    application.add_handler(MessageHandler(filters.CONTACT, register))

    # Запуск бота с использованием уже существующего цикла событий
    application.run_polling()

if __name__ == '__main__':
    main()
