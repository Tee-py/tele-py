from telegram import ( 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    Update, 
    KeyboardButton, 
    ReplyKeyboardMarkup,
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)
import re
import pymongo
from pymongo import MongoClient
import os
import requests
from bs4 import BeautifulSoup
import time
from models2 import *

TOKEN = "1712812245:AAGlUKRs15Ug5ojPrlijhPn0ZqYldORRWf8"
ADD = 1
PORT = 80

def start(bot, update):
    user = update.message.from_user
    chat_id = str(user["id"])
    name = user['first_name']
    trader_exists = Trader.objects(chat_id=chat_id)
    if trader_exists:
        print("This Trader Exists")
        text = f"""
        Welcome, {user["first_name"]} 👋 🎉.\nYour Details exists in our DataBase 🥳.\n\nType / to see the list of commands 🛠 and their uses.
        """
        update.message.reply_text(text=text)
    else:
        try:
            trader = Trader(
                chat_id = chat_id,
                name = name
            )
            trader.save()
            text = f"""
            Welcome, {user["first_name"]} 👋 🎉 🎉.\nYour Details have now been stored with me 🥳.\nYou can proceed to add shitcoins to your portfolio 🚀🚀.\n\nType / to see the lists of commands 🛠 and their uses."""
        except Exception as e:
            print(e)
            text = f"An Error Occured while Trying to Save Your details ❌. Please Try Again."
        update.message.reply_text(text=text)

def add_token(bot, update):
    user = update.message.from_user
    chat_id = str(user["id"])
    trader = Trader.objects(chat_id=chat_id)
    if not trader:
        print("This Trader Does Not Exists")
        text = f"""
        Trader Not Found. Enter /start to register with the Bot.
        """
        update.message.reply_text(text=text)
        return ConversationHandler.END

    message = update.message.text
    if message == "/add":
        text = f"Enter 'CA, name, entry_price' to add a token to your portfolio \n\n(e.g: 0x2456789767, HuskyMeme, 0.123)."
        update.message.reply_text(text=text)
        return ADD 
    
    else:
        try:
            to_list = message.split(", ")
            if len(to_list) < 3:
                text = f"Incomplete Input ❌. Try Again."
                update.message.reply_text(text=text)
                return ADD
            
            token_dict = {
                "owner_id": chat_id,
                "contract_address": to_list[0],
                "name": to_list[1],
                "entry_price": float(to_list[2])
            }
            matching_tokens = Token.objects(contract_address=token_dict['contract_address'])
            if not matching_tokens:
                print("This is a new Token")
                token = Token(**token_dict)
                token.save() 
            text = f"✅ Token Successfully Added."
            update.message.reply_text(text=text)
            return ConversationHandler.END
        except Exception as e:
            print(f"An Error Occured: {e}")
            text = f"An Error Occured while Trying to Add Token ❌. Please Try Again."
            update.message.reply_text(text=text)
            return ConversationHandler.END

def get_portfolio(bot, update):
    user = update.message.from_user
    chat_id = str(user["id"])
    trader = Trader.objects(chat_id=chat_id)
    if not trader:
        print("This Trader Does Not Exists")
        text = f"""
        Trader Not Found. Enter /start to register with the Bot.
        """
        update.message.reply_text(text=text)
    else:
        tokens = Token.objects(owner_id=chat_id)
        if len(tokens) == 0:
            text = f"""
            You have no Token in your portfolio. Enter /add to add a token.
            """
            update.message.reply_text(text=text)
        else:
            for token in tokens:
                bsc_scan_url = f"https://bscscan.com/token/{token.contract_address}"
                pk_url = f"https://info.julswap.com/token/{token.contract_address}"
                jul_url = f"https://pancakeswap.info/token/{token.contract_address}"
                pc_url = f"https://poocoin.app/tokens/{token.contract_address}"
                dx_url = f"https://dex.guru/token/{token.contract_address}-bsc"
                #img_url = "https://bscscan.com/token/images/evdctoken_32.png"
                text = f"Token Name: {token.name}\n\nConract Address: {token.contract_address}\n\nEntry: {token.entry_price}"
                markup = [
                    [InlineKeyboardButton("BSC scan 🚀", url=bsc_scan_url), 
                        InlineKeyboardButton("PancakeSwap 📈", url=pk_url),
                        InlineKeyboardButton("JulSwap 📈", url=jul_url)
                    ], 
                    [InlineKeyboardButton("Poocoin 💹", url=pc_url), InlineKeyboardButton("Dex Guru 🚀", url=dx_url)], 
                    [InlineKeyboardButton("Delete Token 🚮", callback_data=f"d={token.id}")]
                ]
                #bot.send_photo(
                #    chat_id=chat_id, caption=text, photo=img_url, reply_markup=InlineKeyboardMarkup(markup))
                bot.send_message(chat_id=int(chat_id), text=text, reply_markup=InlineKeyboardMarkup(markup))
                print(token.name, token.id)

def button_callback(bot, update):
    chat_id = update.effective_chat.id
    callback_data = update.callback_query.data
    to_list = callback_data.split("=")
    token = Token.objects(id=to_list[1])
    if token:
        token[0].delete()
        text = f"✅ Token Successfully Deleted."
        update.message.reply_text(text=text)
        
def main():
    updater = Updater(TOKEN, use_context=False)
    dispatcher = updater.dispatcher
    conversational_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_token)],
        states={
            #SET_DLS: [MessageHandler(Filters.text, set_dls)],
            #SET_MLS: [MessageHandler(Filters.text, set_mls)],
            ADD: [MessageHandler(Filters.text, add_token)]
        },
        fallbacks=[]
    )
    #dispatcher.add_handler(MessageHandler(Filters.regex('(BUY|SELL|buy|sell|SL|TP|Buy|Sell)+'), broadcast_message))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('portfolio', get_portfolio))
    #dispatcher.add_handler(CommandHandler('disable', disable_updates))
    #dispatcher.add_handler(CommandHandler('details', get_details))
    dispatcher.add_handler(conversational_handler)
    dispatcher.add_handler(CallbackQueryHandler(button_callback))

    #updater.start_polling()
    #updater.start_webhook(listen="0.0.0.0",
    #                      port=int(PORT),
    #                      url_path=TOKEN)
    #updater.bot.setWebhook('https://zizabot.herokuapp.com/' + TOKEN)
    updater.start_webhook(
        listen="0.0.0.0", 
        port=int(PORT), 
        url_path=TOKEN,
        webhook_url=f"https://zizabot.herokuapp.com/{TOKEN}",
    )  
    updater.idle()

if __name__=="__main__":
    main()