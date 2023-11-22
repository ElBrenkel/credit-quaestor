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
def start_command(chat, message):
    """How to start using the bot!
    This command sends first usage instructions.
    """
    mongo_proccessor = MongoProcessor(MongoConnector())
    user = User(message.sender.id, message.sender.name)
    try:
        if not mongo_proccessor.get_data("users", {"id": user.user_id}):
            mongo_proccessor.insert_data("users", user)
    except Exception as ex:
        logging.error("An error has occured: %s", ex)
    chat.send("Welcome to CreditQuaestor! \nType /help to learn how to use me!")


if __name__ == "__main__":
    bot.run()
