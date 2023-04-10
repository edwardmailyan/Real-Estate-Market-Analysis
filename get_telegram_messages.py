from telethon.sync import TelegramClient

import configparser
import csv

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputMessagesFilterUrl

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)

phone = config['Telegram']['phone']

client = TelegramClient(phone, api_id, api_hash)
client.start()

chats = []
last_date = None
size_chats = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=size_chats,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.broadcast or chat.megagroup:
            groups.append(chat)
    except:
        continue

print('Выберите номер группы из перечня:')
i = 0
for с in groups:
    print(str(i) + ' - ' + с.title)
    i += 1
print()

g_index = input("Введите нужную цифру: ")
target_group = groups[int(g_index)]

print('Собираем сообщения...')
all_messages = []
all_messages = client.get_messages(target_group, limit=50000, filter=InputMessagesFilterUrl)

print('Сохраняем данные в файл...')
with open("messages.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['date', 'message'])
    for msg in all_messages:
        if msg.message:
            message = msg.message
        else:
            message = None
        if msg.date:
            date = msg.date
        else:
            date = None
        writer.writerow([date, message])
print('Парсинг сообщений группы успешно выполнен.')
