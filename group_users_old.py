import os
import csv
import sys
import time
import random

import pymysql
import socks
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, UsersTooMuchError, PhoneNumberInvalidError
from time import sleep
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import utils
from telethon import events
from telethon import sync
from utils import username_sql

APP_ID = "337766"
APP_HASH = "c0cd9da9be057008a31af207725a41b4"

# 代理设置
proxy_list = ["64.118.87.28:2447"]
rproxy = random.choice(proxy_list)
host = rproxy.split(":")[0]
port = rproxy.split(":")[1]
proxy = (socks.SOCKS5, host, int(port))


def get_env(name, message, cast=str):
    """把输入的数值加入到环境映象中"""
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
                        # proxy=proxy
                        proxy=None
                        )
try:
    client.start()
except PhoneNumberInvalidError:
    print("Invalid Mobile number,Insert Phone number start with +")
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


print("write in 'users.csv', Please hold....")
while True:
    participants = client(GetParticipantsRequest(
        channel, ChannelParticipantsSearch(''), offset, limit, hash=0
    ))
    time.sleep(20)
    if not participants.users:
        break
    all_participants.extend(participants.users)
    offset += len(participants.users)
    print("extracted : " + str(offset))


def save_db(user):
    """保存到数据库"""
    db = pymysql.connect(host="192.168.52.110", user="superman", password="123456", port=3306, database="tg")
    cursor = db.cursor()
    try:
        cursor.execute(username_sql, (user.id, user.first_name, user.last_name, user.username, user.access_hash, user.bot))
        db.commit()
    except:
        print("----保存到数据库失败----")
        db.rollback()


with open('users.csv', 'a') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, ["id", "first_name", "last_name", "username", "bot"])
    w.writeheader()

    # 写入数据库

    # 保存到csv文件中
    for user in all_participants:
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

print("finish job")
time.sleep(20)
