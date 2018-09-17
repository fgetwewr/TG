import random
import time
import pymysql
from selenium import webdriver
from utils import Utils, phone_numbers_sql, phone_number_sql, phone_update_sql


class Checkphone(object):
    def __init__(self):
        self.url = "https://web.telegram.org/#/login"
        self.db = pymysql.connect(host="192.168.52.110", user="superman", password="123456", port=3306, database="tg")
        self.cursor = self.db.cursor()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(50)
        self.browser.get(self.url)

    def __del__(self):
        self.browser.close()
        self.db.close()

    def get_phone_number(self):
        """获取手机号"""
        self.cursor.execute(phone_numbers_sql)
        total_phone_numbers = self.cursor.fetchone()[0]
        phone_number = 0
        while phone_number < total_phone_numbers:
            self.cursor.execute(phone_number_sql.format(phone_number))
            phone_numbers = self.cursor.fetchall()  # 返回值类型是元祖嵌套元祖
            for phone in phone_numbers:
                if phone[0] is None:
                    return
                print(phone[0])
                # self.add_contact("+86" + phone)
                self.send_keys(phone[0])
                self.parse(phone[0])
            phone_number += 100

    def send_keys(self, phone_number):
        """填充数据并确认"""
        time.sleep(random.randrange(3, 5))
        # browser.find_element_by_xpath("").send_keys()  # country
        self.browser.find_element_by_xpath("//input[@name='phone_country']").clear()
        self.browser.find_element_by_xpath("//input[@name='phone_number']").clear()
        self.browser.find_element_by_xpath("//input[@name='phone_country']").send_keys("+86")  # phone country
        self.browser.find_element_by_xpath("//input[@name='phone_number']").send_keys(phone_number)  # phone number
        self.browser.find_element_by_xpath("//my-i18n[text()='Next']").click()  # 点击下一步
        self.browser.find_element_by_xpath("//span[text()='OK']").click()  # 确认手机号
        time.sleep(random.randrange(3, 5))

    def parse(self, phone_number):
            try:
                self.browser.find_element_by_xpath("//span[@ng-switch-when='PHONE_NUMBER_APP_SIGNUP_FORBIDDEN']")  # 手机号无效或者未注册
                print("You don't have a Telegram account yet, please with Android / iPhone first")
                self.browser.find_element_by_xpath("//span[text()='OK']").click()  # 确认有误退出验证下一个
                self.cursor.execute(phone_update_sql.format(0, 1, phone_number))
                self.db.commit()
                time.sleep(2)
                return
            except Exception as e:
                print(e)
                pass
            try:
                self.browser.find_element_by_xpath("//input[@name='phone_code']")  # 手机号被注册过
                print("This phone number has been registered")
                self.cursor.execute(phone_update_sql.format(1, 1, phone_number))
                self.db.commit()
                self.browser.refresh()
                time.sleep(2)
                return
            except Exception as e:
                print(e)
                pass
            try:
                self.browser.find_element_by_xpath("//span[@ng-switch-when='400']")  # 手机号被封禁
                print("One of the params is missing or invalid.")
                self.browser.find_element_by_xpath("//span[text()='OK']").click()  # 确认有误退出验证下一个
                self.cursor.execute(phone_update_sql.format(0, 1, phone_number))
                self.db.commit()
                time.sleep(2)
                return
            except Exception as e:
                print(e)
                pass
            try:
                self.browser.find_element_by_xpath("//span[@ng-switch-when='420']")  # 请求过于频繁
                print("You are performing too many actions. Please try again later.")
                self.browser.find_element_by_xpath("//span[text()='OK']").click()
                time.sleep(random.randrange(30, 50))
                self.browser.refresh()
                self.get_phone_number()
            except Exception as e:
                print(e)
                pass

    def run(self):
        self.get_phone_number()
        pass


if __name__ == '__main__':
    checkphone = Checkphone()
    checkphone.run()






