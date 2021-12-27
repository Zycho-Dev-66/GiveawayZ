from config import SESSION, API_HASH, API_ID, USERNAME
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from datetime import datetime

Client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
Client.start()

try:
    userlist = Client.iter_participants(USERNAME)
    users = ""

    print("[ACCBOT] {} Retrieved user lists..".format(
        datetime.now().strftime('[ %X ]')))

    for user in userlist:
        users = users + f'{user.id},'
    dbdata = 'users = [' + users + ']'
    with open('database.py', '+w') as db:
        db.write(dbdata)

    print("[ACCBOT] {} User-Verification Database updated..".format(
        datetime.now().strftime('[ %X ]')))

except Exception as e:
    print("Unable to retrieve data.. Error :")
    print(e)
