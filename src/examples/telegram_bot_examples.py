import os

import botogram
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CLIENT_ID = os.environ.get("CLIENT_ID")
bot = botogram.create(BOT_TOKEN)


@bot.command("start")
def start_command(chat, message, args):
    """How to start using the bot!
    This command sends first usage instructions.
    """
    chat.send(
        "Welcome to CreditQuaestor! \nTo start using me please connect with DropBox using the /connectdropbox command!")


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


@bot.command("connectdropbox")
def connectdropbox_command(chat, message):
    redirect_uri = "http://127.0.0.1:5000/authcode"
    authorization_url = f"https://www.dropbox.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code"
    btns = botogram.Buttons()
    btns[0].url("Connect to DropBox", authorization_url)
    chat.send("Please connect me with DropBox!", attach=btns)
 

if __name__ == "__main__":
    bot.run()
