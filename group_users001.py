import os
import re
import random
import sys
import time
import pymysql
from telethon.tl.functions.auth import CheckPasswordRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, UsersTooMuchError, PhoneNumberInvalidError
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError


class Telegram(object):
    def __init__(self, app_id, app_hash):
        self.app_id = app_id
        self.app_hash = app_hash
        self.proxies = ["64.118.87.28:2447", ]
        self.proxy = random.choice(self.proxies)
        self.db = pymysql.connect(host="192.168.52.110", user="superman", password="123456", port=3306, database="tg")
        self.cursor = self.db.cursor()

    def get_phone_and_group(self):
        """获取手机号和群链接"""
        total_phone = " select count(uphone) from myadd_tphone;"
        phone_sql = "select gaddr from myadd_tgroup limit 0, 10;"
        total_channel = " select count(gaddr) from myadd_tgroup;"
        channels = " select gaddr from myadd_tgroup;"
        self.cursor.execute(phone_sql)
        phone_numbers = self.cursor.fetchall()
        return phone_numbers

    def create_client(self):
        """创建客户端"""
        client = TelegramClient(os.environ.get('TG_SESSION', 'printer'), self.app_id, self.app_hash, proxy=None).start()
        # try:
        #     client.start()
        # except PhoneNumberInvalidError:
        #     print("Invalid Mobile number,Insert Phone number start with +")
        #     exit()
        return client

    def join_group(self, client):
        """加入群"""
        try:
            print(sys.argv[1])  # 从外部获得要加入的群链接
        except IndexError:
            print("Please set group link as argument if you want add new group")
        try:
            client(ImportChatInviteRequest(sys.argv[1]))
        except (UserAlreadyParticipantError, IndexError, FloodWaitError, UsersTooMuchError) as e:
            print("Error join group")
            print(e)

    def add_contact(self, client):
        """添加手机号联系人"""

        # sql = 'insert into myadd_tphone (uphone, paddr, mark) values ("13245678934","郑州", 0);'
        sql = "update myadd_tphone set mark=1 where id=0;"
        self.cursor.execute(sql)
        self.db.commit()
        return "add contact success"

    def add_group_or_channel(self, client):
        """加入群组或频道"""
        pass

    def get_group_list(self, client):
        """获取现有群列表"""
        channel_names = [d.name for d in client.get_dialogs() if d.is_group]
        for idx, ch in enumerate(channel_names):
            print(idx + 1, ch)
        avail_channels = [d.entity for d in client.get_dialogs() if d.is_group]
        return avail_channels

    def get_user_info(self, avail_channels, client):
        """获取群成员信息"""
        offset = 0
        limit = 100
        all_participants = []
        print("Start get user info, Please hold...")
        # channel_index = input("Please select number of super group you want to scrape> ")
        for channel in avail_channels:
            while True:
                participants = client(GetParticipantsRequest(
                    channel, ChannelParticipantsSearch(''), offset, limit, hash=0
                ))
                time.sleep(20)
                if not participants.users:
                    break
                user = participants.users
                self.connect_mysql(user)
                all_participants.extend(participants.users)
                offset += len(participants.users)
                print("extracted : " + str(offset))
            print("群%s成员提取成功".format(channel))
        print("所有的群成员提取成功")

    def connect_mysql(self, user):
        """和MySQL数据库进行对接"""
        sql = "insert into myadd_guser(user_id, first_name, last_name, user_name, user_hash, user_phone, user_bot) values (%s, %s, %s, %s, %s, %s, %s);"
        try:
            self.cursor.execute(sql, (
            user.id, user.first_name, user.last_name, user.username.user.access_hash, user.phone, user.bot))
            self.db.commit()
        except:
            self.db.rollback()

    def run(self):
        # client = self.create_client()
        phone_numbers = self.get_phone_and_group()
        for number in phone_numbers:
        #     # self.add_contact(client)
            print(number[0])
        # avail_channels = self.get_group_list(client)
        # self.get_user_info(avail_channels, client)
        #
        add_phone_result = self.add_contact("a")
        print(add_phone_result)
        self.db.close()


if __name__ == '__main__':
    # 要判断用户输入的内容
    # app_id = int(input("请输入app_id:"))
    # app_hash = input("请输入app_hash:")
    telegram = Telegram(358839, "81e79f358ac94d6459dc8a199668e66f")
    telegram.run()
