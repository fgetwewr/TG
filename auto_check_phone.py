import re
import time

from telethon import TelegramClient
from telethon.tl.functions.auth import CheckPhoneRequest


class Phonecontact(TelegramClient):
    def checkPhone(self, phone, no=None):
        phone = self.parse_phone(phone)
        res = self(CheckPhoneRequest(phone_number=phone))
        if no:
            print(no, phone, res.phone_registered)
        else:
            print(phone, res.phone_registered)
        return res.phone_registered

    def parse_phone(self, phone):
        if isinstance(phone, int):
            return str(phone)
        else:
            phone = re.sub(r'[+()\s-]', '', str(phone))
            if phone.isdigit():
                return phone

#
# client = MyTG('zbsb', api_id, api_hash)
# client.connect()
#
# d = '''
# 12345678
# 23456789
# 34567890'''
# d = d.split()
# for n, i in enumerate(d):
#     phone = i
#     client.checkPhone(phone, n + 1)
