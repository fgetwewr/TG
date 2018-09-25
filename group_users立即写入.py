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

APP_ID = "362716"
APP_HASH = "1d8cfdc2afe9d9b6888b878ac7697de3"

proxy_list = ["127.0.0.1:8888", ]
rproxy = random.choice(proxy_list)
host = rproxy.split(":")[0]
port = rproxy.split(":")[1]
proxy = (socks.SOCKS5, host, int(port))


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
                        proxy=proxy
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


# client.run_until_disconnected()#
print("write in 'users.csv'")

with open('users.csv', 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, ["id", "first_name", "last_name", "username", "bot"])
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
            w.writerow({"id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "username": user.username,
                        "bot": user.bot,
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
print("finish")
time.sleep(20)
