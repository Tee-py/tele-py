from telethon.sync import TelegramClient
from telethon import events

api_id = 2342197
api_hash = "df090ff21d4f144a373f65f1f77873f3"
phone = '+2348156269921'
client = TelegramClient(phone, api_id, api_hash)

def forward_messages_to_users(id_list, message):
    for user_id in id_list:
        message.forward_to(user_id)
        print("Forwarded")

@client.on(events.NewMessage)
async def main(event):
    message = event.original_update.message
    message.forward_to(chat)
    print(message.message)
    print(message.media)
    await forward_message_to_users(id_list, message)
    #print('{}'.format(event))
    #entity = client.get_entity(some_id)
    #await client.send_message('1', 'Hello to myself!')

@client.on(events.NewMessage(pattern="start"))
def start(event):
    message = event.message
    print(message)
    try:
        sent_by_id = message.peer_id.PeerUser.user_id
        with client.conversation(sent_by_id) as conv:
            prompt = conv.send_message('Please Enter the Passcode to register with us.')
            code = conv.get_response()
            if code == "12345":
                conv.send_message('Successfull.')
            else:
                conv.send_message('Error.')

    except:
        print("This is not a user!!")
    #async with client.conversation(event.)

with client:
    client.start()
    client.run_until_disconnected()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

#
#if not client.is_user_authorized():
#    client.send_code_request(phone)
#    client.sign_in(phone, input('Enter the code: '))

