# #设置浏览器参数
# def setOptions(headless=False, noimage=True, nocss=False, nojs=False):
#     boptions = Options()
#     if headless:
#         boptions.add_argument('--headless')
#         boptions.add_argument('--disable-gpu')
#     if noimage:
#         ''' chrome
#         prefs = {'profile.default_content_setting_values': {
#             'images': 2,
#             'falush':2,
#          }
#         }
#         boptions.add_experimental_option("prefs", prefs)
#         '''
#         ''' firefox '''
#         boptions.set_preference('permissions.default.image',2)
#         boptions.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
#     if nojs:
#         '''
#         prefs = {
#             'profile.default_content_setting_values': {
#                 'javascript': 2,
#             }
#         }
#         boptions.add_experimental_option("prefs", prefs)
#         '''
#         boptions.set_preference('permissions.default.javascript', 2)
#     if nocss:
#         '''
#         prefs = {
#             'profile.default_content_setting_values': {
#                 'css': 2,
#             }
#         }
#         boptions.add_experimental_option("prefs", prefs)
#         '''
#         boptions.set_preference('permissions.default.stylesheet', 2)
#     return boptions
#
# #重置代理
# def setProxy(boptions):
#     time.sleep(1)
#     proxy = getProxyAddr()
#     #log.info("proxy %s", proxy)
#     boptions.add_argument("--proxy-server=" + proxy)
#     return boptions
#
# from utils import utils
# from selenium import webdriver
# from selenium.webdriver import DesiredCapabilities
# from selenium.webdriver.common.proxy import Proxy
# from selenium.webdriver.common.proxy import ProxyType
#
# proxy = Proxy(
#     {
#         'proxyType': ProxyType.MANUAL,
#         'httpProxy': '{}'.format(utils.get_proxy())  # 代理ip和端口
#     }
# )
# # 新建一个“期望技能”，哈哈
# desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# # 把代理ip加入到技能中
# proxy.add_to_capabilities(desired_capabilities)
# driver = webdriver.PhantomJS(
#     # executable_path="D:\projectdata\TG\venv\Scripts\phantomjs.exe",
#     desired_capabilities=desired_capabilities
# )
# # 测试一下
# driver.get('http://httpbin.org/ip')
# print(driver.page_source)
#
# # 现在开始切换ip
# # 再新建一个ip
# proxy = Proxy(
#     {
#         'proxyType': ProxyType.MANUAL,
#         'httpProxy': '{}'.format(utils.get_proxy())  # 代理ip和端口
#     }
# )
# # 再新建一个“期望技能”，（）
# desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# # 把代理ip加入到技能中
# proxy.add_to_capabilities(desired_capabilities)
# # 新建一个会话，并把技能传入
# driver.start_session(desired_capabilities)
# driver.get('http://httpbin.org/ip')
# print(driver.page_source)
# driver.close()

import multiprocessing
import time


class Students(object):
    """创建学生类"""
    def __init__(self, number):
        print("---" + number + "---")
        time.sleep(1)


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)
    result = []
    for i in range(10):
        msg = "hello %d" % (i)
        result.append(pool.apply_async(Students, (msg,)))
    pool.close()
    pool.join()
    for res in result:
        print(res)
    print("Sub-process(es) done.")





