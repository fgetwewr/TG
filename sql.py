import pymysql


class Getdata(object):
    def __init__(self):
        self.db = pymysql.connect(host="192.168.52.110", user="superman", password="123456", port=3306, database="tg")
        self.cursor = self.db.cursor()


    def get_phone_number(self):
        total_phone_sql = "select count(uphone) from myadd_tphone;"
        self.cursor.execute(total_phone_sql)
        total_phone_umber = self.cursor.fetchone()[0]
        print(total_phone_umber)
        num = 0
        while num < total_phone_umber:
            phone_sql = "select uphone from myadd_tphone limit {}, 100;".format(num)
            self.cursor.execute(phone_sql)
            phone_numbers = self.cursor.fetchall()  # 返回值类型是元祖嵌套元祖
            num += 100
            print(phone_numbers)
            return phone_numbers

    def get_channels(self):
        total_channel_sql = "select count(gaddr) from myadd_tgroup;"
        self.cursor.execute(total_channel_sql)
        total_channel_umber = self.cursor.fetchone()[0]
        print(total_channel_umber)
        num = 0

        while num < total_channel_umber:
            phone_sql = "select gaddr from myadd_tgroup limit {}, 100;".format(num)
            self.cursor.execute(phone_sql)
            chanels = self.cursor.fetchall()  # 返回值类型是元祖嵌套元祖
            num += 100
            print(chanels)
        return chanels


data = Getdata()
data.get_phone_number()
data.get_channels()
