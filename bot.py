from telegram.ext import Updater, CommandHandler
import requests
import re

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
    text = """Welcome To Tee-py Telegram Bot 👋.
    I am Here to send you random Dog Images from the internet.👍

    enter: /dog to get a random Dog Image from the internet.
    """
    update.message.reply_text(text=text)

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