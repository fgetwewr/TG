import random
import time
import pymysql
from selenium import webdriver
from utils import utils, phone_numbers_sql, phone_number_sql, phone_update_sql


class Checkphone(object):
    def __init__(self):
        self.url = "https://web.telegram.org/#/login"
        self.db = pymysql.connect(host="192.168.52.110", user="superman", password="Caoke123#", port=3306, database="tg")
        self.cursor = self.db.cursor()
        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.add_argument('--proxy-server=http://{}'.format(utils.get_proxy()))  # 设置代理
        # self.chromeOptions.add_argument('content-Type:"application/x-www-form-urlencoded}"')  # 设置请求头的内容格式
        # try:
        self.browser = webdriver.Chrome(chrome_options=self.chromeOptions)
        # except:
        #     self.__init__()
        # self.browser = webdriver.Chrome()  # content-Type:application/x-www-form-urlencoded
        self.browser.implicitly_wait(50)
        self.browser.get(self.url)
        print(self.browser.current_url)

    def __del__(self):
        self.browser.close()
        self.db.close()

    def get_phone_number(self):
        """获取手机号"""
        self.cursor.execute(phone_numbers_sql)
        total_phone_numbers = self.cursor.fetchone()[0]
        if total_phone_numbers is None:
            return
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
            self.__init__()
            phone_number += 8

    def send_keys(self, phone_number):
        """填充数据并确认"""
        time.sleep(random.randrange(3, 5))
        # browser.find_element_by_xpath("").send_keys()  # country
        self.browser.find_element_by_xpath("//input[@name='phone_country']").clear()
        self.browser.find_element_by_xpath("//input[@name='phone_number']").clear()
        self.browser.find_element_by_xpath("//input[@name='phone_country']").send_keys("+86")  # phone country
        self.browser.find_element_by_xpath("//input[@name='phone_number']").send_keys(phone_number)  # phone number
        time.sleep(random.uniform(1, 2))
        self.browser.find_element_by_xpath("//my-i18n[text()='Next']").click()  # 点击下一步
        time.sleep(random.uniform(2, 4))
        self.browser.find_element_by_xpath("//span[text()='OK']").click()  # 确认手机号
        time.sleep(random.randrange(3, 5))

    def parse(self, phone_number):
        """结果处理"""
        try:
            try:
                self.browser.find_element_by_xpath(
                    "//span[@ng-switch-when='PHONE_NUMBER_APP_SIGNUP_FORBIDDEN']") or self.browser.find_element_by_xpath(
                    "//span[@ng-switch-when='400']")  # 手机号无效、未注册或者是封禁
                print(
                    "You don't have a Telegram account yet, please with Android / iPhone first or One of the params is missing or invalid" + "---->" + phone_number)
                self.browser.find_element_by_xpath("//span[text()='OK']").click()  # 确认有误退出验证下一个
                self.cursor.execute(phone_update_sql.format(0, 1, phone_number))
                self.db.commit()
                time.sleep(2)
                return
            except Exception as e:
                print(e)
                self.db.rollback()
                pass
            try:
                self.browser.find_element_by_xpath("//span[@ng-switch-when='420']")  # 请求过于频繁,不修改数据库
                print("You are performing too many actions. Please try again later." + "---->" + phone_number)
                self.browser.find_element_by_xpath("//span[text()='OK']").click()
                # time.sleep(random.randrange(30, 50))  # 隐式等待可以代替
                # self.browser.refresh()
                self.browser.close()
                self.__init__()
                self.get_phone_number()
            except Exception as e:
                print(e)
                self.db.rollback()
                pass
            try:
                self.browser.find_element_by_xpath("//input[@name='phone_code']")  # 手机号被注册过
                print("This phone number has been registered" + "---->" + phone_number)
                self.cursor.execute(phone_update_sql.format(1, 1, phone_number))
                self.db.commit()
                self.browser.refresh()
                time.sleep(2)
                return
            except Exception as e:
                print(e)
                self.db.rollback()
                pass
        except Exception as e:
            print(e)
            self.browser.refresh()
            self.get_phone_number()
            pass

    def run(self):
        self.get_phone_number()
        pass


if __name__ == '__main__':
    checkphone = Checkphone()
    checkphone.run()






