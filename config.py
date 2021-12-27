import os
from os import getenv
from dotenv import load_dotenv

dirlist = os.listdir()

for file in dirlist:
    try:
        filename, filext = os.path.splitext(file)
        if filext == ".env":
            load_dotenv(file)
    except:
        pass

try:
    TOKEN = getenv('TOKEN')
    API_ID = getenv('API_ID')
    API_HASH = getenv('API_HASH')
    SESSION = getenv('SESSION')
    TEAM = getenv('TEAM')
    IMAGE = getenv('IMAGE')
    GROUP = getenv('GROUP_1')
    GROUP2 = getenv('GROUP_2')
    GROUP3 = getenv('GROUP_3')
    USERNAME = getenv('USERNAME_1')
    USERNAME2 = getenv('USERNAME_2')
    USERNAME3 = getenv('USERNAME_3')
    OWNER = getenv('OWNER')
    PROOFS_ID = getenv('PROOFS_ID')
    PROOFS_USERNAME = getenv('PROOFS_CHANNEL')
    ABOUT = getenv('ABOUT')
    HOWTO_HEADER = getenv('HOWTO_HEADER')
    HOWTO_CONTEXT = getenv('HOWTO_CONTEXT')
    HOWTO_FOOTER = getenv('HOWTO_FOOTER')
    MONGODB = getenv('MONGODB_URI')
    ACC_LIST = list(map(str, getenv('ACC_LIST').split()))
    POINT_LIST = list(map(int, getenv('POINT_LIST').split()))
except Exception as e:
    print(e)
