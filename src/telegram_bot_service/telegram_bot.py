import os
import logging
import botogram
from dotenv import load_dotenv
from src.data_objects.user import User
from src.mongo.mongo_processor import MongoProcessor
from src.mongo.mongo_connector import MongoConnector

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = botogram.create(BOT_TOKEN)


@bot.command("start")
def start_command(chat):
    """How to start using the bot!
    This command sends first usage instructions.
    """
    chat.send(
        "Welcome to CreditQuaestor! \nTo start using me please register using the /register command!"
    )


@bot.command("register")
def connectdropbox_command(chat, message):
    """Register to our service!
    This command registers you to the service.
    """
    mongo_proccessor = MongoProcessor(MongoConnector())
    user = User(message.sender.id, message.sender.name)
    try:
        if not mongo_proccessor.get_data("users", {"id": user.user_id}):
            mongo_proccessor.insert_data("users", user)
            chat.send("Registration complete!")
        else:
            logging.info("already registerd.")
            chat.send(
                "You are already registered, lets begin! \nUse the /help command to view further options."
            )
    except Exception as ex:
        chat.send("Registration failed :( \nPlease try again.")
        logging.error("An error has occured: %s", ex)


if __name__ == "__main__":
    bot.run()
