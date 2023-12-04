import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from src.data_objects.user import User
from src.mongo.mongo_processor import MongoProcessor
from src.mongo.mongo_connector import MongoConnector
from src.telegram_bot_service.add_transaction import IS_ROUTINE, conv_handler

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

IS_ROUTINE, TRANSACTION_TYPE, AMOUNT, DATE, DESCRIPTION = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mongo_proccessor = MongoProcessor(MongoConnector())

    user = update.effective_user
    user_id = user.id
    user_name = user.username if user.username else user.first_name
    user = User(user_id, user_name)

    try:
        if not mongo_proccessor.get_data("users", {"id": user.user_id}):
            mongo_proccessor.insert_data("users", user)
    except Exception as ex:
        logging.error("An error has occured: %s", ex)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to CreditQuaestor! \nType /help to learn how to use me!",
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)

    application.add_handler(start_handler)

    application.run_polling()
