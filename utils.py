# coding:utf-8
import os
import random
import sys
import time
import logging
import pymysql
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, UsersTooMuchError, PhoneNumberInvalidError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.contacts import GetContactsRequest, ImportContactsRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.auth import CheckPasswordRequest

phone_numbers_sql = "select count(uphone) from myadd_tphone;"
group_numbers_sql = "select count(gaddr) from myadd_tgroup;"
phone_update_sql = "update myadd_tphone set mark={} where uphone={};"

phone_number_sql = "select uphone from myadd_tphone limit {}, 100;"
group_number_sql = "select gaddr from myadd_tgroup limit {}, 100;"

phone_number = 0
group_number = 0
contacts_list = []


class Utils(object):
    def __init__(self):
        pass

    def proxies(self):
        """代理IP"""
        proxies = ["64.118.87.28:2447", ]
        proxy = random.choice(proxies)
        return proxy


# utils = Utils()
