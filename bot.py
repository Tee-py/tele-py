from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationalHandler, CallbackContext
import requests
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from db import DataBase, User

REGISTER = 0
DOG = 1

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    return contents["url"]

def greet(bot, update):
    chat_id = update.message.chat_id
    exists, user = User.chat_id_exists(chat_id)
    if exists:
        text = f"""Hi {user["name"]} 👋.
        I am Here to send you random Dog Images from the internet.👍

        Enter /dog to get any random dog image.
        """
        update.message.reply_text(text=text)
        return DOG
    text = """Welcome To Tee-py Telegram Bot 👋.
    I am Here to send you random Dog Images from the internet.👍

    Type anyname you would love to be associated with here.
    """
    update.message.reply_text(text=text)
    return REGISTER

def register(bot, update):
    chat_id = update.message.chat_id
    name = update.message.text
    user = User(name=name, chat_id=chat_id)
    user.save()
    text = f"""
    Welcome, {name} 👋.
    You can now start getting random dog images from the internet.
    To get random images, Enter /dog.
    """
    update.message.reply_text(text=text)
    return DOG

def dog(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    print(chat_id)
    bot.send_photo(chat_id=chat_id, photo=url)

def main():
    updater = Updater(KEY, use_context=False)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('dog', dog))
    dp.add_handler(CommandHandler('start', greet))
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()