import pymysql
import requests
from bs4 import BeautifulSoup
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, UsersTooMuchError, PhoneNumberInvalidError
from time import sleep
import os
import csv
import sys
import time
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import utils
from telethon import events
from telethon import sync
import time
import random
import socks
import utils
from utils import username_sql

APP_ID = "365847"
APP_HASH = "46fe393febe53876dd3267a6aff47c15"


def get_proxy():
    """获取代理IP"""
    # response = requests.get("http://127.0.0.1:5000/random")
    # proxy = BeautifulSoup(response.text, "lxml").get_text()
    # response = requests.get("https://web.telegram.org")
    # if response.status_code != 200:
    #     self.get_proxy()
    proxy_list = [" 218.248.73.193:1080", "5.56.133.131:1080"]
    proxy = random.choice(proxy_list)
    # response = requests.get("https://web.telegram.org")
    # if response.status_code != 200:
    #     proxy = random.choice(proxy_list)
    host = proxy.split(":")[0]
    port = proxy.split(":")[1]
    proxy = (socks.SOCKS5, host, int(port))
    print("--"*80)
    print(proxy)
    print("--"*80)
    return proxy


def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


client = TelegramClient(os.environ.get('TG_SESSION', 'printer'), APP_ID, APP_HASH,
                        # get_env('TG_API_ID', 'Enter your API ID: ', int),
                        # get_env('TG_API_HASH', 'Enter your API hash: '),
                        # proxy=get_proxy(),
                        proxy=None,
                        )
try:
    client.start()
except PhoneNumberInvalidError:
    print("Invalid Mobile number,Insert Phone number start with +")
    client.disconnect()
    exit()
try:
    print(sys.argv[1])

except IndexError:
    print("Please set group link as argument if you want add new group")

offset = 0
limit = 100
all_participants = []

try:
    client(ImportChatInviteRequest(sys.argv[1]))
except (UserAlreadyParticipantError, IndexError, FloodWaitError, UsersTooMuchError) as e:
    print("Error join group")
    print(e)

channel_names = [d.name for d in client.get_dialogs() if d.is_group]
for idx, ch in enumerate(channel_names):
    print(idx + 1, ch)

avail_channels = [d.entity for d in client.get_dialogs() if d.is_group]
channel_index = input("Please select number of super group you want to scrape> ")
# channel = client.get_entity(PeerChannel(avail_channels[int(channel_index)]))
channel = avail_channels[int(channel_index) - 1]

# entity = client.get_entity('@gamegeek2')
# peer = client.get_input_entity('@gamegeek2')
# client(SendMessageRequest(PeerUser("@gamegeek2"), 'hello'))
# channel = client.get_entity(PeerChannel("@akharikhabar"))
# channel="@akharikhabar"#PeerChannel("@akharikhabar")
# channel="@testmissyou"
# if channel.startswith("@"):
#	print("you can get user list of groups only or channel if you are admin")
#	exit()
# client(JoinChannelRequest(channel))
# client.send_message('@gamegeek2', 'Hello World from Telethon!')


# client.run_until_disconnected()#

def save_db(user):
    """保存到数据库"""
    db = pymysql.connect(host="192.168.52.110", user="superman", password="Caoke123#", port=3306, database="tg", charset="utf8")
    cursor = db.cursor()
    try:
        cursor.execute(username_sql, (user.id, user.first_name, user.last_name, user.username, user.access_hash, user.bot))
        db.commit()
    except Exception as e:
        print(e)
        print("----保存到数据库失败----")
        db.rollback()


print("write in 'users.csv'")
with open('users.csv', 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, ["user_id", "first_name", "last_name", "username", "user_hash", "user_phone", "bot"])
    w.writeheader()

    while True:
        participants = client(GetParticipantsRequest(
            channel, ChannelParticipantsSearch(''), offset, limit, hash=0
        ))
        time.sleep(20)
        if not participants.users:
            break
        all_participants.extend(participants.users)
        for user in all_participants[offset:]:
            save_db(user)
            w.writerow({
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "user_hash": user.access_hash,  # 用户hash值
                "user_phone": user.phone,
                "bot": user.bot,  # 判断是机器人还是用户
                        })
        f.flush()
        offset += len(participants.users)
        print("extracted : " + str(offset))
    # users=participants.users
# print(participants.users)
# print(users)
# ufile=open("users.txt","w")


# ufile.write(user.stringify())
# print(user.stringify())
print("----finish----")
client.disconnect()
time.sleep(20)
print("----time sleep over----")

