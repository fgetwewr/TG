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
from telethon.utils import parse_phone

phone_numbers_sql = "select count(uphone) from myadd_tphone where checked=0;"  # 手机号总数
group_numbers_sql = "select count(gaddr) from myadd_tgroup;"  # 群链接的总数
phone_update_sql = "update myadd_tphone set mark={},checked={} where uphone={};"  # 更新手机号

phone_number_sql = "select uphone from myadd_tphone where checked=0 limit {}, 100;"  # 手机号
group_number_sql = "select gaddr from myadd_tgroup limit {}, 100;"  # 群链接地址

# 用户信息
username_sql = "insert into myadd_guser(user_id, first_name, last_name, user_name, user_hash, user_phone, user_bot) values (%s, %s, %s, %s, %s, %s, %s);"


class Utils(object):
    def __init__(self):
        pass

    def proxies(self):
        """代理IP"""
        proxies = ["64.118.87.28:2447", ]
        proxy = random.choice(proxies)
        return proxy

    def headers(self):
        """请求头"""
        headers = [{"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Mobile Safari/537.36"},
                   ]
        header = random.choice(headers)
        return header


# utils = Utils()
# constants.py  常量