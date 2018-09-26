from utils import *
logging.ERROR()
logger = logging.getLogger(__name__)


class Telegram(object):
    def __init__(self, app_id, app_hash):
        # self.proxy = Utils().proxies()  # 代理IP
        self.db = pymysql.connect(host="192.168.52.110", user="superman", password="123456", port=3306, database="tg")
        self.cursor = self.db.cursor()
        try:
            self.client = TelegramClient(os.environ.get('TG_SESSION', 'printer'), app_id, app_hash, proxy=None).start()
            # self.client.
        except PhoneNumberInvalidError:
            print("Invalid Mobile number,Insert Phone number start with +")
            exit()

    def __del__(self):
        self.db.close()
        # self.client.disconnect()  # 关闭客户端连接

    def get_phone(self):
        """获取手机号"""
        self.cursor.execute(phone_numbers_sql)
        total_phone_numbers = self.cursor.fetchone()[0]
        phone_number = 0
        while phone_number < total_phone_numbers:
            self.cursor.execute(phone_number_sql.format(phone_number))
            phone_numbers = self.cursor.fetchall()  # 返回值类型是元祖嵌套元祖
            for phone in phone_numbers:
                print(phone[0])
                # self.add_contact("+86" + phone)
                if phone[0] is None:
                    return
            phone_number += 100
    print("添加手机联系人完成")

    def get_group(self):
        """获取群连接"""
        self.cursor.execute(group_numbers_sql)
        total_group_numbers = self.cursor.fetchone()[0]
        group_number = 0
        while group_number < total_group_numbers:
            self.cursor.execute(group_number_sql.format(group_number))
            group_numbers = self.cursor.fetchall()
            for group in group_numbers:
                print(group[0])
                # self.join_group(group[0])
                if group[0] is None:
                    return
            group_number += 100
        print("添加群组完成")

    def join_group(self, group):
        """加入群"""
        try:
            print(sys.argv[1])  # 从外部获得要加入的群链接
        except IndexError:
            print("Please set group link as argument if you want add new group")
        try:
            self.client(ImportChatInviteRequest(sys.argv[1]))
        except (UserAlreadyParticipantError, IndexError, FloodWaitError, UsersTooMuchError) as e:
            print("Error join group")
            print(e)

    def add_contact(self, phone):
        """添加手机号联系人"""
        contacts_list = []
        try:
            contacts_list.append(InputPhoneContact(client_id=0, phone=phone, first_name="", last_name=""))
        except:
            return "add contact failure"
        else:
            result = self.client(ImportContactsRequest(contacts_list))
            self.cursor.execute(phone_update_sql.format(True, phone))
            self.db.commit()
            return result + "\n" + "导入联系人成功"

    def add_group_or_channel(self):
        """加入群组或频道"""
        return "add channel success"

    def get_group_list(self):
        """获取现有群列表"""
        channel_names = [d.name for d in self.client.get_dialogs() if d.is_group]
        for idx, ch in enumerate(channel_names):
            print(idx + 1, ch)
        avail_channels = [d.entity for d in self.client.get_dialogs() if d.is_group]
        return avail_channels

    def get_user_info(self, avail_channels):
        """获取群成员信息"""
        offset = 0
        limit = 100
        all_participants = []
        print("Start get user info, Please hold...")
        # channel_index = input("Please select number of super group you want to scrape> ")
        for channel in avail_channels:
            while True:
                participants = self.client(GetParticipantsRequest(
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
        try:
            self.cursor.execute(username_sql, (
            user.id, user.first_name, user.last_name, user.username, user.access_hash, user.bot))
            self.db.commit()
        except:
            self.db.rollback()

    def run(self):
        # client = self.create_client()
        # total_channel, total_phone = self.get_phone_and_group()
        # for number in phone_numbers:
        #     # self.add_contact(client)
        #     print(number[0])
        # print("total_phone:", total_phone)
        # print("total_channel:", total_channel)
        # avail_channels = self.get_group_list(client)
        # self.get_user_info(avail_channels, client)
        #
        # add_phone_result = self.add_contact("a")
        # print(add_phone_result)
        self.get_phone()
        self.get_group()


if __name__ == '__main__':
    # 要判断用户输入的内容
    # app_id = int(input("请输入app_id:"))
    # app_hash = input("请输入app_hash:")
    telegram = Telegram(365847, "46fe393febe53876dd3267a6aff47c15")
    telegram.run()


