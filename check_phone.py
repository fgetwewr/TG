import random
import time
import pymysql
from selenium import webdriver
import threading, queue
from utils import utils, phone_numbers_sql, phone_number_sql, phone_update_sql


class Checkphone(object):
    def __init__(self):
        self.url = "https://web.telegram.org/#/login"
        self.db = pymysql.connect(host="192.168.52.110", user="superman", password="Caoke123#", port=3306, database="tg")
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def reset_proxy(self):
        """重置IP代理"""
        proxy = utils.get_proxy()
        print("---"*80)
        print(proxy)
        print("---"*80)
        return proxy

    def browser_set(self, proxy):
        """构建浏览器"""
        # Chrome浏览器
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--proxy-server=http://{}'.format(proxy))  # 设置代理
        browser = webdriver.Chrome(chrome_options=chromeOptions)
        # self.chromeOptions.add_argument('content-Type:"application/x-www-form-urlencoded}"')  # 设置请求头的内容格式

        # IE浏览器,pass
        # IeOptions = webdriver.ie
        # browser = webdriver.Ie()

        browser.maximize_window()
        browser.implicitly_wait(15)  # 隐式等待
        return browser

    def get_phone_number(self, browser):
        """获取手机号"""
        print("----正在查询数据库----")
        self.cursor.execute(phone_numbers_sql)
        total_phone_numbers = self.cursor.fetchone()[0]
        if total_phone_numbers is None:
            print("----数据库没有数据----")
            return
        phone_number = 0
        while phone_number < total_phone_numbers:
            self.cursor.execute(phone_number_sql.format(phone_number))
            phone_numbers = self.cursor.fetchall()  # 返回值类型是元祖嵌套元祖
            for phone in phone_numbers:
                if phone[0] is None:
                    print("----数据库数据已经验证完成---")
                    return
                print(phone[0])
                # self.add_contact("+86" + phone)
                self.send_keys(phone[0], browser)
                self.parse(phone[0], browser)
            phone_number += 200

    def send_keys(self, phone_number, browser):
        """填充数据并确认"""
        print("----正在填充数据----")
        try:
            # 国家根据区号就可以判断
            browser.find_element_by_xpath("//input[@name='phone_country']").clear()
            browser.find_element_by_xpath("//input[@name='phone_number']").clear()
            browser.find_element_by_xpath("//input[@name='phone_country']").send_keys("+86")  # phone country
            browser.find_element_by_xpath("//input[@name='phone_number']").send_keys(phone_number)  # phone number

            time.sleep(random.uniform(2, 3))
            browser.find_element_by_xpath("//my-i18n[text()='Next']").click()  # 点击下一步
            time.sleep(random.uniform(2, 3))
            browser.find_element_by_xpath("//span[text()='OK']").click()  # 确认手机号
            print("----正在验证数据----")
            time.sleep(random.uniform(3, 5))
        except:
            print("----请求URL超时请求新的浏览器----")
            browser.close()
            self.run()

    def parse(self, phone_number, browser):
        """结果处理"""
        print("----正在进行结果处理----")
        try:
            browser.find_element_by_xpath(
<<<<<<< HEAD
                    "//span[@ng-switch-when='PHONE_NUMBER_APP_SIGNUP_FORBIDDEN']") and browser.find_element_by_xpath(
                "//span[@ng-switch-when='400']")  # 手机号无效、未注册或者是封禁
            print("You don't have a Telegram account yet, please with Android / iPhone first or One of the params is missing or invalid" + "---->" + phone_number)
=======
                    "//span[@ng-switch-when='PHONE_NUMBER_APP_SIGNUP_FORBIDDEN']") or browser.find_element_by_xpath(
                "//span[@ng-switch-when='400']")  # 手机号无效、未注册或者是封禁
            print(
                "You don't have a Telegram account yet, please with Android / iPhone first or One of the params is missing or invalid" + "---->" + phone_number)
>>>>>>> e95855aaf8cdc4a9045e16c04c6893314d2bc921
            browser.find_element_by_xpath("//span[text()='OK']").click()  # 确认有误退出验证下一个
            self.cursor.execute(phone_update_sql.format(0, 1, phone_number))
            self.db.commit()
            return
        except Exception as e:
            print(e)
            self.db.rollback()
            pass
        try:
            browser.find_element_by_xpath("//input[@name='phone_code']")  # 手机号被注册过
            print("This phone number has been registered" + "---->" + phone_number)
            self.cursor.execute(phone_update_sql.format(1, 1, phone_number))
            self.db.commit()
            browser.refresh()
            return
        except Exception as e:
            print(e)
            self.db.rollback()
            pass
        print("----结果异常请求新的浏览器----")
        browser.close()
        self.run()

    def run(self):
        # pool = multiprocessing.Pool(processes=4)
        # for i in range(10):
        #     proxy = pool.apply_async(self.reset_proxy())
        #     browser = pool.apply_async(self.browser_set(proxy)) v
        #     browser.get(self.url)
        #     self.get_phone_number(browser)
        # pool.close()
        # pool.join()
        # print("Sub-process(es) done.")

        proxy = self.reset_proxy()
        browser = self.browser_set(proxy)
        print("----请求新的URL----")
        browser.get(self.url)
        self.get_phone_number(browser)


if __name__ == '__main__':
    checkphone = Checkphone()
    checkphone.run()
    # checks = [Checkphone().run() for i in range(4)]



'''
利用队列解决查询数据库重复的问题
'''




