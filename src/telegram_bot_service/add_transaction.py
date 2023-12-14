import logging
from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from src.data_objects.transaction import TransactionSchema
from src.mongo.mongo_processor import MongoProcessor
from src.mongo.mongo_connector import MongoConnector

# TODO: Use the same logger from the main file
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

(
    AMOUNT,
    DESCRIPTION,
    ROUTINE_DECISION,
    IS_ROUTINE,
    DATE,
    RECURRENCE_TYPE,
    START_DATE,
    END_DATE,
) = range(8)

transaction = {}
routine = {}


async def start_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user for transaction type"""
    reply_keyboard = [["INCOME", "SPENDING"]]
    transaction["user_id"] = update.effective_user.id
    await update.message.reply_text(
        "Please select transaction type: INCOME / SPENDING "
        "Send /cancel to stop talking to me.\n\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="INCOME / SPENDING",
        ),
    )

    return AMOUNT


async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected transaction type and asks amount."""
    transaction["transaction_type"] = update.message.text
    logger.info("%s was selected", update.message.text)
    await update.message.reply_text(
        "Please input transaction amount ",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DESCRIPTION


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the amount and asks for description."""
    transaction["amount"] = update.message.text
    logger.info("Amount: %s", update.message.text)
    await update.message.reply_text("Please add a description for the transaction.")

    return ROUTINE_DECISION


async def routine_decision(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the description and asks if routine."""
    transaction["description"] = update.message.text
    logger.info("Description: %s", update.message.text)

    reply_keyboard = [["Yes", "No"]]
    await update.message.reply_text(
        "Is this a recurring transaction?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Yes / No",
        ),
    )
    return IS_ROUTINE


async def is_routine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Checks if routine and diverts accordingly."""
    has_routine = bool(update.message.text == "Yes")
    logger.info("Routine: %s", is_routine)

    if has_routine:
        reply_keyboard = [["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]]
        await update.message.reply_text(
            "How often does it occur?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                input_field_placeholder="DAILY / WEEKLY / MONTHLY / YEARLY",
            ),
        )
        return RECURRENCE_TYPE

    await update.message.reply_text(
        "Insert date (2024-08-19 format), /skip to use today",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DATE


async def date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the date."""
    transaction["transaction_date"] = update.message.text
    logger.info("date: %s", update.message.text)
    await end_transaction(update, transaction, "Transaction added!")
    return ConversationHandler.END


async def skip_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inserts todays date."""
    logger.info("Default today was decided.")
    await end_transaction(update, transaction, "Transaction added with today's date!")
    return ConversationHandler.END


async def recurrence_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the recurrence type and asks for start date."""
    routine["time_frame"] = update.message.text
    logger.info("time_frame: %s", update.message.text)
    await update.message.reply_text(
        "Please insert start date (2024-08-19 format). use /skip to use today.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return START_DATE


async def start_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the start date."""
    routine["start_date"] = update.message.text
    logger.info("start date: %s", update.message.text)
    await update.message.reply_text("Please insert end date (2024-08-19 format).")

    return END_DATE


async def skip_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inserts todays date as start date."""
    logger.info(
        "Default today was decided: %s",
        datetime.strftime(datetime.date.today(), "%Y-%m-%d"),
    )
    await update.message.reply_text("Please insert end date (2024-08-19 format).")

    return END_DATE


async def end_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the end date."""
    routine["end_date"] = update.message.text
    routine["default_amount"] = transaction["amount"]
    transaction["routine"] = routine
    logger.info("date: %s", update.message.text)
    await end_transaction(update, transaction, "Routine transaction added!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text("Transaction addition canceled.")

    return ConversationHandler.END


async def end_transaction(update: Update, trans, message):
    transaction_object = TransactionSchema().load(trans)
    mongo_proccessor = MongoProcessor(MongoConnector())
    mongo_proccessor.insert_data("Transactions", transaction_object)
    await update.message.reply_text(message)


add_transaction_handler = ConversationHandler(
    entry_points=[CommandHandler("add", start_add)],
    states={
        AMOUNT: [MessageHandler(filters.Regex("^(INCOME|SPENDING)$"), amount)],
        DESCRIPTION: [MessageHandler(filters.Regex("^\d+(\.\d+)?$"), description)],
        ROUTINE_DECISION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, routine_decision)
        ],
        IS_ROUTINE: [MessageHandler(filters.Regex("^(Yes|No)$"), is_routine)],
        DATE: [
            MessageHandler(filters.Regex("\d{4}-\d{2}-\d{2}"), date),
            CommandHandler("skip", skip_date),
        ],
        RECURRENCE_TYPE: [
            MessageHandler(
                filters.Regex("^(DAILY|WEEKLY|MONTHLY|YEARLY)"), recurrence_type
            )
        ],
        START_DATE: [
            MessageHandler(filters.Regex("\d{4}-\d{2}-\d{2}"), start_date),
            CommandHandler("skip", skip_start_date),
        ],
        END_DATE: [MessageHandler(filters.Regex("\d{4}-\d{2}-\d{2}"), end_date)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
