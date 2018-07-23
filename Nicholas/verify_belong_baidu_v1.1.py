from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import paramiko
import os
import time

yuming = 'C:/Users/George/Desktop/yuming/1.txt' #域名库文件
host = "142.234.162.99" #服务器host
root = "root"   #账号
password = "free@0516" #密码
remotepath = '/www/wwwroot/xbw/' #远程提交路径
localpath = 'E:/PyCode/baidutijiao/down/'    #本地上传路径
path = "C:/Chrome/chromedriver.exe" #谷歌控制器路径

print('正在连接服务器')
transport = paramiko.Transport(host, 22)
transport.connect(username=root, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)  # 如果连接需要密钥，则要加上一个参数，hostkey="密钥"
print('服务器连接成功')

file = open(yuming)
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': localpath}
options.add_experimental_option('prefs', prefs)  #更改下载地址
driver = webdriver.Chrome(path,chrome_options=options)  # 打开 Chrome 浏览器
print('打开登录页面')
driver.get("https://ziyuan.baidu.com/login/index?u=/site/index")

print('百度批量验证程序开始执行~')
driver.find_element_by_id('site-add-btn').click()
while 1:
    lines = file.readlines(100000)
    if not lines:
        break
    for url in lines:
        pass
        print('当前提交url :' + url)
        print('更改协议头')
        http = driver.find_element_by_xpath("//div[@id='protocolSelect']/input")
        driver.execute_script("arguments[0].value = 'http://'", http)
        time.sleep(0)
        driver.find_element_by_class_name('add-site-input').send_keys(url)
        driver.find_element_by_id('site-add').click()
        time.sleep(1)
        while 1:
            start = time.clock()
            try:
                driver.find_element_by_id('sub-attr').click()
                print('检测到新域名。继续验证')
                end = time.clock()
                break
            except:
                print("该域名已经提交请替换域名!")
        print('后退浏览器')
        driver.back()
        print('再次点击添加网站')
        time.sleep(1)
        while 1:
            start = time.clock()
            try:
                driver.find_element_by_id('site-add').click()
                print('破解成功成功')
                end = time.clock()
                break
            except:
                print("破解百度验证规则中，请等待!")
        print('确认域名领域')
        time.sleep(1)
        driver.find_element_by_id('sub-attr').click()
        print('开始下载验证文件')

        while 1:
            start = time.clock()
            try:
                driver.find_element_by_xpath("//dd[@id='file']/p[2]/a[1]").click()
                print('已定位到元素')
                end = time.clock()
                break
            except:
                print("还未定位到元素!")
        print('定位耗费时间：' + str(end - start))
        time.sleep(3)
        filename = os.listdir(localpath)
        print('已找到下载文件' + filename[0])

        print('上传本地文件')
        sftp.put(localpath + filename[0], remotepath + filename[0])  # 将本地的文件上传至服务器/www/wwwroot/
        time.sleep(4)
        my_file = localpath + filename[0]
        if os.path.exists(my_file):
            print('删除本地下载文件')
            os.remove(localpath + filename[0])
        else:
            print('文件没有删除')
        print('开始验证服务器文件')
        driver.find_element_by_id('verifySubmit').click();
        while 1:
            start = time.clock()
            try:
                driver.find_element_by_id("dialog").click()
                print('验证成功')
                end = time.clock()
                break
            except:
                print("正在验证中，请等待!")
        driver.get("https://ziyuan.baidu.com/site/siteadd");
transport.close()  # 关闭连接
print('服务器链接关闭')
