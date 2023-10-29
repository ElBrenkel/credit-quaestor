import os

import botogram
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = botogram.create(BOT_TOKEN)


@bot.command("start")
def hello_command(chat, message, args):
    """Say hello to the world!
    This command sends "Hello world" to the current chat
    """
    chat.send("shkarim sheli")


@bot.command("spam")
def spam_command(chat, message, args):
    """Send a spam message to this chat"""
    btns = botogram.Buttons()
    btns[0].callback("Delete this message", "delete")

    chat.send("This is spam!", attach=btns)


@bot.callback("delete")
def delete_callback(query, chat, message):
    message.delete()
    query.notify("Spam message deleted. Sorry!")


@bot.command("survey")
def survey_command(chat, message, args):
    """Reply to a simple survey!"""
    btns = botogram.Buttons()
    btns[0].callback("Great", "notify", "Happy to hear that!")
    btns[1].callback("Not so great", "notify", "I'm sorry! What happened?")

    chat.send("How are you feeling?", attach=btns)


@bot.callback("notify")
def notify_callback(query, data, chat, message):
    query.notify(data)


if __name__ == "__main__":
    bot.run()
