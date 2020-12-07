from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update


def broadcast_message(bot, update):
    message = update.message.text
    print(message)
    update.message.reply_text(text=message)
    bot.send_message(chat_id="1256735190", text=message)






def main():
    updater = Updater("1432662407:AAGqtsCjDmepId-U5PiZOkjvspLCcmGkGrM", use_context=False)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.regex('(Signal|signal)?'), broadcast_message))
    updater.start_polling()
    updater.idle()


if __name__=="__main__":
    main()