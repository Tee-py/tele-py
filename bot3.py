from telethon.sync import TelegramClient
from telethon import events 
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from datetime import datetime
import pytz

api_id = 2342197
api_hash = "df090ff21d4f144a373f65f1f77873f3"
phone = '+2348156269921'
client = TelegramClient(phone, api_id, api_hash)
fauna_client = FaunaClient(secret="fnAD-TjtVUACCNpkor-UvokJnvfq9DrZS8dTC8eQ")

def forward_messages_to_users(id_list, message):
    for user_id in id_list:
        message.forward_to(user_id)
        print("Forwarded")

@client.on(events.NewMessage)
async def main(event):
    message = event.original_update.message
    #entity = client.get_entity("385705779")
    #res = await message.forward_to(entity)
    await client.send_message('385705779', 'Yello to myself!')
    print(message.message)
    print(message.media)
    #forward_message_to_users(id_list, message)
    #print('{}'.format(event))
    #entity = client.get_entity(some_id)
    #await client.send_message('1', 'Hello to myself!')

@client.on(events.NewMessage(pattern="start"))
async def start(event):
    message = event.message
    #print(event)
    try:
        from_id = message.from_id.user_id
        sent_by_id = message.peer_id.user_id
        async with client.conversation(sent_by_id) as conv:
            prompt = await conv.send_message(f"Welcome 👋. Please Enter passcode 🔑 to start receiving signal updates.")
            code = await conv.get_response()
            #print(code)
            if code.message == "12345":
                try:
                    fauna_client.query(q.get(q.match(q.index("users"), sent_by_id)))
                    await conv.send_message(f"""
                    Welcome, 👋 🎉.\nYour Details exists in our DataBase 🥳.\nYou can now start recieving signal updates.""")
                except Exception as e:
                    #print(e)
                    try:
                        user = fauna_client.query(q.create(q.collection("users"), {
                            "data": {
                            "id": sent_by_id,
                            "date": datetime.now(pytz.UTC)
                            }
                        }))
                        await conv.send_message('Successfull.')
                    except Exception as e:
                        print(e) 
                        await conv.send_message('An Error Occurred while saving your details.')            
            else:
                await conv.send_message('Error.')

    except Exception as e:
        print(e)
        print("This is not a user!!")
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

