from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from db import DataBase, User, BotUser


SET_DLS = 0

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

def get_details(bot, update):
    chat_id = update.message.from_user["id"]
    user = BotUser.retrieve(chat_id)
    update.message.reply_text(
        text=f"""name: {user.name}\nDefault lot size: {user._dls}\nMax loss per trade: {user._max_loss}\nSignal status: {user.can_receive_signals}\n\nEnter: /set_dls to change Default lot size\n    /set_mls to change Max loss per trade\n    /disable to disable signal updates\n    /enable to enable signal updates
        """
        )

def set_dls(bot, update):
    message = update.message.text
    reply = [[10.0, 1.0, 0.1, 0.01]]
    if message == "/set_dls":
        update.message.reply_text(
            text="Choose the LotSize you want to set or Enter your custom value",
            reply_markup=ReplyKeyboardMarkup(reply, one_time_keyboard=True),
        )
        return SET_DLS
    try:
        message = float(message)
    except:
        update.message.reply_text(
            text="Invalid Input For LotSize.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    if message in reply[0]:
        chat_id = update.message.from_user["id"]
        user = BotUser.retrieve(chat_id)
        user._dls = float(message)
        user.save()
        update.message.reply_text(
            text="Successfully updated default lot size for trades. enter /details to see your details.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        if message<0.01 or message > 100:
            update.message.reply_text(
                text="LotSize must be between 0.01 and 100 both inclusive.",
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END
        chat_id = update.message.from_user["id"]
        user = BotUser.retrieve(chat_id)
        user._dls = message
        user.save()
        update.message.reply_text(
            text="Successfully updated default lot size for trades. enter /details to see your details.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

def start(bot, update):
    user = update.message.from_user
    print(update.message.text)
    if User.chat_id_exists(user["id"]):
        text = f"""
        Welcome, {user["first_name"]} 👋.\nYour Details exists in our DataBase.\n\nType / to see the list of commands and their uses.
        """
        update.message.reply_text(text=text)
    else:
        to_store = BotUser(name=user["first_name"], chat_id=user["id"])
        to_store.save()
        text = f"""
        Welcome, {user["first_name"]} 👋.\nYour Details have now been stored in our database.\nYou are now able to receive Forex Signals sent to the Signal Group\n\nType / to see the lists of commands and their uses."""
        update.message.reply_text(text=text)

def main():
    updater = Updater("KEY", use_context=False)
    dispatcher = updater.dispatcher
    conversational_handler = ConversationHandler(
        entry_points=[CommandHandler('set_dls', set_dls)],
        states={
            SET_DLS: [MessageHandler(Filters.text, set_dls)],
        },
        fallbacks=[]
    )
    dispatcher.add_handler(MessageHandler(Filters.regex('(BUY|SELL|buy|sell|SL|TP|Buy|Sell)+'), broadcast_message))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('enable', enable_updates))
    dispatcher.add_handler(CommandHandler('disable', disable_updates))
    dispatcher.add_handler(CommandHandler('details', get_details))
    dispatcher.add_handler(conversational_handler)
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()