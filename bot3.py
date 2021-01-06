from telethon.sync import TelegramClient
from telethon import events 
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from datetime import datetime
import pytz
import re
import os

api_id = int(os.environ.get('TELETHON_API_ID'))
api_hash = os.environ.get('API_HASH')
phone = os.environ.get('TELETHON_PHONE')
secret = os.environ.get('FAUNA_SECRET_KEY')
client = TelegramClient(phone, api_id, api_hash)
fauna_client = FaunaClient(secret=secret)


@client.on(events.NewMessage(pattern=re.compile(r"(sell|buy)+", re.I)))
async def broadcast(event):
    #Get the Signal
    message = event.original_update.message
    try:
        #Trying to know if message is coming from a channel
        c_id = message.peer_id.channel_id
        print(c_id)
        message = message.message
    except:
        pass
    #Get All Subscribers
    all_subscribers = fauna_client.query(
        q.paginate(q.documents(q.collection('users')))
    )
    #Start sending messages
    for subscriber in all_subscribers['data']:
        user = fauna_client.query(q.get(q.ref(q.collection("users"), subscriber.__dict__["value"]["id"])))
        text = f"NEW SIGNAL UPDATE 💰📶🔊📣🚀‼️‼️\n\n{message}"
        await client.send_message(user["data"]["chat_id"], text)  

@client.on(events.NewMessage(pattern=re.compile(r"start", re.I)))
async def start(event):
    message = event.message
    try:
        from_id = message.from_id.user_id
        sent_by_id = message.peer_id.user_id
        async with client.conversation(sent_by_id) as conv:
            prompt = await conv.send_message(f"Welcome 👋. Please Enter passcode 🔑 to start receiving signal updates.")
            code = await conv.get_response()
            if code.message == "12345":
                try:
                    fauna_client.query(q.get(q.match(q.index("chat_id"), sent_by_id)))
                    await conv.send_message(f"""
                    Welcome, 👋 🎉.\nYour Details exists in our DataBase 🥳.\nYou can now start recieving signal updates.""")
                except Exception as e:
                    try:
                        user = fauna_client.query(q.create(q.collection("users"), {
                            "data": {
                            "chat_id": sent_by_id,
                            "date": datetime.now(pytz.UTC)
                            }
                        }))
                        await conv.send_message(f"""
                        Welcome 👋 🎉 🎉.\nYour Details have now been stored in our database 🥳.\nYou are now able to receive Forex Signals sent to the Signal Group 🚀🚀.""")
                    except Exception as e:
                        await conv.send_message('An Error Occurred while saving your details😞😭. Please Try Again.')            
            else:
                await conv.send_message(f"Invalid Passcode ❌. Contact Admin For Passcode.")

    except Exception as e:
        await conv.send_message('An Error Occurred while saving your details😞😭. Please Try Again.')    
    #async with client.conversation(event.)

with client:
    client.start()
    client.run_until_disconnected()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

#indexes = fauna_client.query(q.paginate(q.indexes()))
#print(indexes)

#
#if not client.is_user_authorized():
#    client.send_code_request(phone)
#    client.sign_in(phone, input('Enter the code: '))


#all_subscribers = fauna_client.query(
#    q.paginate(q.documents(q.collection('users')))
#)
#print(all_subscribers)
#first = all_subscribers["data"][0]
#result = fauna_client.query(
#  q.select("data", q.get(q.collection("users")))
#)
#user = fauna_client.query(q.get(q.ref(q.collection("users"), first.__dict__["value"]["id"])))
#print(user)
#print(result)
#print(first)
#print(fauna_client.query(q.get(q.ref(q.collection("users"), all_subscribers['data'][0].id))))