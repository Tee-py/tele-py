from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import pymongo
from pymongo import MongoClient
import os
import requests
from bs4 import BeautifulSoup
import time



PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ.get('TOKEN', "1432662407:AAGqtsCjDmepId-U5PiZOkjvspLCcmGkGrM")

client = MongoClient()
database = client.lmsbot
events = database.events

data = {
    "username": "oemmanuel683",
    "password": "Kelechi@2000",
    "rememberusername": 1
}

def extractLoginTokenFromPage(session):
    LoginGetPage = session.get("https://lms.ui.edu.ng/login/index.php")
    soup = BeautifulSoup(LoginGetPage.content, 'html.parser')
    all_inputs = soup.find_all("input")
    loginTokenInput = list(filter(lambda input: input["name"]=="logintoken", all_inputs))[0]
    return loginTokenInput["value"]


def get_timelines(payload):
    session = requests.session()
    payload["logintoken"] = extractLoginTokenFromPage(session)
    dashboard = session.post("https://lms.ui.edu.ng/login/index.php", data=payload)
    if "Oluwatobi Emmanuel" in str(dashboard.content):
        print("Login Successfull")
    soup = BeautifulSoup(dashboard.content, 'html.parser')
    calender = soup.find_all("div", class_="event")
    return [
        {
            "title": day.find_all("a")[0].text,
            "date": day.find_all("a")[1].text
        } for day in calender
    ]

def new_timelines(payload, bot):
    timelines = get_timelines(data)
    new = list(filter(lambda event:events.find_one({"title": event["title"]})==None, timelines))
    if new:
        events.insert_many(new)
        print("Got A New One")
        text = f"NEW EVENTS 🚀🚀🚀‼️‼️\n\n"
        for event in new:
            text += f"\nDATE: {timelines[1]['date']}\nTITLE: {timelines[1]['title']}\n"
        bot.send_message("1256735190", text=text)
    else:
        print("Nothing New")




def get_events(bot, update):
    update.message.reply_text(text="Fetching Events...")
    print(update.message.chat.id)
    try:
        timelines = get_timelines(data)
        new = list(filter(lambda event:events.find_one({"title": event["title"]})==None, timelines))
        print(new)
        if new:
            events.insert_many(new)
        text = f"UPCOMING EVENTS 🚀🚀🚀‼️‼️\n\n"
        print(timelines)
        for event in timelines:
            text += f"\nDATE: {timelines[1]['date']}\nTITLE: {timelines[1]['title']}\n"
        update.message.reply_text(text=text)
    except Exception as e:
        print(e)
        update.message.reply_text(text="An Error Occured. Please Try Again.")
    


def start(bot, update):
    user = update.message.from_user
    message = update.message.text
    text = f"Welcome {user['first_name']}👋. Please Enter / to see the list of commands the Bot Accepts."
    update.message.reply_text(text=text)
        

        
def main():
    updater = Updater(TOKEN, use_context=False)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('events', get_events))
    updater.start_polling()
    while True:
        new_timelines(data, updater.bot)
        #updater.bot.send_message("1256735190", text="Hello World!! Welcome.")
        time.sleep(300)
    #updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    #updater.bot.setWebhook('https://zizabot.herokuapp.com/' + TOKEN)  
    updater.idle()

if __name__=="__main__":
    main()