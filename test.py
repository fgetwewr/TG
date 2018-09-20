#设置浏览器参数
def setOptions(headless=False, noimage=True, nocss=False, nojs=False):
    boptions = Options()
    if headless:
        boptions.add_argument('--headless')
        boptions.add_argument('--disable-gpu')
    if noimage:
        ''' chrome
        prefs = {'profile.default_content_setting_values': {
            'images': 2,
            'falush':2,
         }
        }
        boptions.add_experimental_option("prefs", prefs)
        '''
        ''' firefox '''
        boptions.set_preference('permissions.default.image',2)
        boptions.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    if nojs:
        '''
        prefs = {
            'profile.default_content_setting_values': {
                'javascript': 2,
            }
        }
        boptions.add_experimental_option("prefs", prefs)
        '''
        boptions.set_preference('permissions.default.javascript', 2)
    if nocss:
        '''
        prefs = {
            'profile.default_content_setting_values': {
                'css': 2,
            }
        }
        boptions.add_experimental_option("prefs", prefs)
        '''
        boptions.set_preference('permissions.default.stylesheet', 2)
    return boptions

#重置代理
def setProxy(boptions):
    time.sleep(1)
    proxy = getProxyAddr()
    #log.info("proxy %s", proxy)
    boptions.add_argument("--proxy-server=" + proxy)
    return boptions