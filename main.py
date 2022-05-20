from telethon.sync import TelegramClient

from telethon import events
import requests

from config import api_id, api_hash, \
    alert_chat, test_chat, \
    api_alert_enable as alert_enable, api_alert_disable as alert_disable, api_alert_location as alert_location

client = TelegramClient('me', api_id, api_hash)
client.start()


# прослушка смс
@client.on(events.NewMessage(chats=[test_chat, alert_chat]))
async def handler(event):
    if event.sender_id == alert_chat or event.sender_id == test_chat:

        response = requests.get(alert_location)

        msg = event.message.message
        arr = event.message.message.split(" ")

        # print(arr)

        # dangerLevel: NORMAL
        if arr[0] == "🟢":
            level = "NORMAL"
            print("🟢")
            for i in arr:
                if i[0].isupper() and i != 'Відбій':
                    print(i)
                    requests.post(alert_disable,
                                  data={
                                      "dangerLevel": level,
                                      "title": f"{i}"
                                  }
                                  )
                    print(response.status_code)

        # dangerLevel: MEDIUM
        if arr[0] == "🟡":
            level = "MEDIUM"
            print("🟡")
            if arr[2] == '':
                del arr[2]
                for i in arr:
                    if i[0].isupper() and i != 'Повітряна' and i != 'Відбій':
                        print(i)


            elif arr[2] != '':
                for i in arr:
                    if i[0].isupper() and i != 'Повітряна':
                        print(i)

        # dangerLevel: HIGH
        if arr[0] == "🔴":
            level = "HIGH"
            print("🔴")
            for i in arr:
                if i[0].isupper() and i != 'Повітряна':
                    print(i)
                    requests.post(alert_enable, data={
                        "dangerLevel": level,
                        "title": f"{i}"
                    })


try:
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
finally:
    client.disconnect()

with client:
    client.loop.run_until_complete(handler())
