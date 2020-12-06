from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update


def broadcast_message(bot, update):
    message = update.message.text
    print(message)
    bot.sen