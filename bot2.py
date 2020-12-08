from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from db import DataBase, User, BotUser

def broadcast_message(bot, update):
    message = update.message.text
    all_users = User.db.retrieve_collection("User")
    for user in all_users:
        if user["signal_enabled"]:
            bot.send_message(chat_id=user["chat_id"], text=message)

def disable_updates(bot, update):
    chat_id = update.message.from_user["id"]
    user = BotUser.retrieve(chat_id)
    user.can_receive_signals = False
    user.save()
    update.message.reply_text(
        text="You have currently Disabled updates feature. Enter /enable to start getting signal updates."
        )

def enable_updates(bot, update):
    chat_id = update.message.from_user["id"]
    user = BotUser.retrieve(chat_id)
    user.can_receive_signals = True
    user.save()
    update.message.reply_text(
        text="You have currently Enabled updates feature. Enter /disable to stop getting updates."
        )

def start(bot, update):
    user = update.message.from_user
    if User.chat_id_exists(user["id"]):
        text = f"""
        Welcome, {user["first_name"]} 👋.
        Your Details exists in our DataBase.
        
        Type / to see the list of commands and their uses.
        """
        update.message.reply_text(text=text)
    else:
        to_store = BotUser(name=user["first_name"], chat_id=user["id"])
        to_store.save()
        text = f"""
        Welcome, {user["first_name"]} 👋.
        Your Details have now been stored in our database.
        You are now able to receive Forex Signals sent to the Signal Group

        Type / to see the lists of commands and their uses.
        """
        update.message.reply_text(text=text)

def main():
    updater = Updater("1432662407:AAGqtsCjDmepId-U5PiZOkjvspLCcmGkGrM", use_context=False)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.regex('(BUY|SELL|buy|sell|SL|TP|Buy|Sell)+'), broadcast_message))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('enable', enable_updates))
    dispatcher.add_handler(CommandHandler('disable', disable_updates))
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()