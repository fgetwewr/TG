import re
import time

from utils import utils
import socks
from telethon import TelegramClient
from telethon.tl.functions.auth import CheckPhoneRequest


class Phonecontact(TelegramClient):
    def checkPhone(self, phone, no=None):
        phone = self.parse_phone(phone)
        res = self(CheckPhoneRequest(phone_number=phone))
        print(res)
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


rproxy = utils.get_proxy()
host = rproxy.split(":")[0]
port = rproxy.split(":")[1]
proxy = (socks.SOCKS5, host, int(port))
print(proxy)

api_id = 365847
api_hash = "46fe393febe53876dd3267a6aff47c15"

client = Phonecontact('check', api_id, api_hash, proxy=proxy)
client.connect()

d = '''
1 
13300000985
13300000986
13300000987
13300000988
13300000989
13300000990
13300000991
13300000992
13300000993
'''
d = d.split()
for n, i in enumerate(d):
    phone = i
    # print(n, "--------", i)
    # client.checkPhone(phone, n + 1)
    client.checkPhone(phone)

