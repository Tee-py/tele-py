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
    #print('{}'.format(event))
    #entity = client.get_entity(some_id)
    #await client.send_message('1', 'Hello to myself!')



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

