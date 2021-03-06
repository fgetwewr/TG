# coding:utf-8
import os
import random
import sys
import time
import logging
import pymysql
import requests
from bs4 import BeautifulSoup
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

phone_numbers_sql = "select count(phone) from myAdd_guangxi where checked=0;"  # 手机号总数
group_numbers_sql = "select count(gaddr) from myadd_tgroup;"  # 群链接的总数
phone_update_sql = "update myAdd_guangxi set mark={},checked={} where phone={};"  # 更新手机号

phone_number_sql = "select phone from myAdd_guangxi where checked=0 limit {}, 200;"  # 手机号
group_number_sql = "select gaddr from myadd_tgroup limit {}, 100;"  # 群链接地址

# 清空数据库，自动增长键归零
sql = "truncate table table_name;"

# 用户信息
username_sql = "insert into myAdd_guser(user_id, first_name, last_name, user_name, user_hash, user_bot) values (%s, %s, %s, %s, %s, %s);"


class Utils(object):
    def __init__(self):
        pass

    def headers(self):
        """请求头"""
        headers = [{"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Mobile Safari/537.36"},
                   ]
        header = random.choice(headers)
        return header

    def get_proxy(self):
        """获取代理IP"""
        response = requests.get("http://127.0.0.1:5000/random")
        proxy = BeautifulSoup(response.text, "lxml").get_text()
        response = requests.get("https://web.telegram.org")
        if response.status_code != 200:
            self.get_proxy()
        return proxy


utils = Utils()
# constants.py  常量
