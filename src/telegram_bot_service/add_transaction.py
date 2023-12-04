import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

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
    RECUURENCE_TYPE,
    START_DATE,
    END_DATE,
) = range(8)

transaction = {}


async def start_tramsaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
        return RECUURENCE_TYPE
    else:
        return DATE


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
        PHOTO: [
            MessageHandler(filters.PHOTO, photo),
            CommandHandler("skip", skip_photo),
        ],
        LOCATION: [
            MessageHandler(filters.LOCATION, location),
            CommandHandler("skip", skip_location),
        ],
        BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
