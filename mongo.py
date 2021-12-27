from pymongo import MongoClient
from config import MONGODB, OWNER
from datetime import datetime
from time import strftime, sleep

print("[ACCBOT] {} Initializing MongoDB..".format(
    datetime.now().strftime('[ %X ]')))

uri_str_start = MONGODB.find('//')
uri_str_end = MONGODB.find('@')

uri_str = MONGODB[uri_str_start+2:uri_str_end]
uri_sep = uri_str.find(':')

uri_user = uri_str[0:uri_sep]
uri_pass = uri_str[uri_sep:len(uri_str)]
print("[ACCBOT] {} Parsed MongoDB URI..".format(
    datetime.now().strftime('[ %X ]')))

try:
    start = datetime.now()
    client = MongoClient(MONGODB)
    end = datetime.now()

    con_ping = (end-start).microseconds / 1000

    print("""[ACCBOT] {} Successfully connected to the mongodb cluster..
>> Connection username : {}
>> Connection password : {}

Status : CONNECTION_SUCCESS
Ping   : {}ms\n\n""".format(datetime.now().strftime('[ %X ]'), uri_user, uri_pass, con_ping))

except Exception as e:
    print("""[ACCBOT] {} Failed to connect to the mongodb cluster..
>> Connection username : {}
>> Connection password : {}

Error : {}

Status : CONNECTION_FAILED
Ping   : {}\n\n""".format(datetime.now().strftime('[ %X ]'), uri_user, uri_pass, e, con_ping))

db = client["accbot"]
print("[ACCBOT] {} Initialized Database..".format(
    datetime.now().strftime('[ %X ]')))

users = db["users"]
print("[ACCBOT] {} Initialized Collection..".format(
    datetime.now().strftime('[ %X ]')))

admins = users.find({"status": "admin"})
admin_count = 0
admin_list = ""
for i in admins:
    admin_list = admin_list + i["username"] + '\n'
    admin_count = admin_count + 1

print("[ACCBOT] {} MongoDB Bot Admins Count : {}".format(
    datetime.now().strftime('[ %X ]'), admin_count))

if admin_count == 0:
    print("[ACCBOT] {} Setting MongoDB Admin..".format(
        datetime.now().strftime('[ %X ]')))
    owner = {
        "username": OWNER,
        "wallet": 1000,
        "reflist": [
            "admin-mode"
        ],
        "status": "admin",
        "withdrawals": ["admin-mode"]
    }
    dev = {
        "username": "Zycho_66",
        "wallet": 1000,
        "reflist": [
            "admin-mode"
        ],
        "status": "admin",
        "withdrawals": ["admin-mode"]
    }
    users.insert_many([owner, dev])
    print("[ACCBOT] {} MongoDB Bot Admin : {}".format(
        datetime.now().strftime('[ %X ]'), OWNER))
else:

    print("[ACCBOT] {} MongoDB Bot Admins list :".format(
        datetime.now().strftime('[ %X ]')))
    print(admin_list)
