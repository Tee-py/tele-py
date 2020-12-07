from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from db import DataBase, User

def broadcast_message(bot, update):
    message = update.message.text
    all_users = User.db.retrieve_collection("User")
    for user in all_users:
        bot.send_message(chat_id=user["chat_id"], text=message)

def start(bot, update):
    user = update.message.from_user
    to_store = User(name=user["first_name"], chat_id=user["id"])
    to_store.save()
    text = f"""
    Welcome, {user["first_name"]} 👋.
    Your Details have now been stored in our database.
    You will now be able to get Signals sent to the group.
    """
    update.message.reply_text(text=text)


def main():
    updater = Updater("1432662407:AAGqtsCjDmepId-U5PiZOkjvspLCcmGkGrM", use_context=False)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.regex('(Signal|signal)+'), broadcast_message))
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()