# -*- coding=utf-8 -*-
import os
import platform
import time
from selenium import webdriver

local = os.path.normcase(os.path.abspath('.')) #项目相对路径
localpath = local + '/down/'    #本地上传路径

yuming = local + '/yuming/yuming.txt' #域名库文件
pre_txt = local + '/yuming/news_pre.txt' #选择你要批量修改的域名类型
sysstr = platform.system()
if sysstr =="Windows":
    path = local + "/driver/chromedriver.exe"  # 谷歌控制器路径
    profile = 'C:/Users/username/AppData/Local/Google/Chrome/User Data/test_profile'

else:
    path = local + "/driver/chromedriver"  # 谷歌控制器路径
    profile = '/Users/YV/Library/Application Support/Google/Chrome/Default'

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': localpath, 'profile.managed_default_content_settings.images': 2}
options.add_argument("--user-data-dir="+profile)
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(path, chrome_options=options)  # 打开 Chrome 浏览器
driver.implicitly_wait(6)   # seconds

yumingfile = open(yuming, "r+")

def login(driver):
    print('请登录')
    driver.get("https://ziyuan.baidu.com/login/index?u=/?castk=LTE%3D")
    driver.get_cookies()
    print("登陆成功,并成功记录登录状态")

driver.get("https://ziyuan.baidu.com/site/batchadd?mainsite=")
yuming_file = open(yuming)
# driver.maximize_window()
pre_file = open(pre_txt)
while 1:
    lines = yuming_file.readlines(100000)
    preline = pre_file.readlines(100000)
    if not lines:
        break
    for url in lines:
        urlno = url.split('\n', 1)[0]
        print('开始批量添加子站')
        sendurl= driver.find_element_by_class_name('select-domain')
        sendurl.click()
        sendurl.send_keys(url)
        print('正在生成' + urlno + '子站的域名文件夹')
        sonsitefile = open(local + '/sonsite/' + urlno + '.txt', 'a')
        print('正在生成' + urlno + '主域名的子站url')
        if not preline:
            break
        for pre in preline:
            a = pre.split('\n', 1)[0]
            print('url:http://' + a + url[3:])
            sonsitefile.write('http://' + a + url[3:])
        print('url:'+url+"文件生成完毕")
        sonsitefile.close()
        send_pre_url = driver.find_element_by_id('batchaddTextarea')
        send_pre_url.click()
        print('正在打开url:'+local + '/sonsite/' + urlno + '.txt')
        a = open(local + '/sonsite/' + urlno + '.txt')
        data = a.read()
        send_pre_url.send_keys(data)
        driver.find_element_by_id('batchaddSiteBtn').click()
        time.sleep(0.5)
        driver.find_element_by_class_name('btn-mid-blue').click()
print('生成完毕,结束程序')
# login(driver)
