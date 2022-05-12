from telethon.sync import TelegramClient

from telethon import events

from config import api_id, api_hash, alert_chat, test_chat

client = TelegramClient('me', api_id, api_hash)
client.start()


# прослушка смс
@client.on(events.NewMessage(chats=[test_chat, alert_chat]))
async def handler(event):
    status = {
        "danger": "Повітряна тривога",
        "safe": "Відбій тривоги",
        "attention": "Зверніть увагу, тривога ще триває у"
    }

    if event.sender_id == alert_chat or event.sender_id == test_chat:
        msg = event.message.message
        arr = event.message.message.split(' ')

        print(msg)


try:
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
finally:
    client.disconnect()

with client:
    client.loop.run_until_complete(handler())
